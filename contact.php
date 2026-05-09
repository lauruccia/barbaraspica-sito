<?php
/**
 * Form contatti - barbaraspica.it
 * Invio via SMTP autenticato (Serverplan)
 *
 * Per evitare di dover installare PHPMailer/Composer su un cPanel senza shell,
 * questo file include un mini-client SMTP scritto a mano (~150 righe).
 * Funziona con SSL (porta 465) e con STARTTLS (porta 587).
 */

// ============================================================
// CONFIGURAZIONE
// ============================================================
$CONFIG = [
    // SMTP Serverplan
    'smtp_host'     => 'mail.barbaraspica.it',
    'smtp_port'     => 465,
    'smtp_secure'   => 'ssl',     // 'ssl' (porta 465) o 'tls' (porta 587)
    'smtp_user'     => 'info@barbaraspica.it',
    'smtp_pass'     => 'H5zL{-]fUws?Uya2',  // ⚠️ vedi note in fondo

    // Indirizzi
    'to'            => 'info@barbaraspica.it',
    'to_name'       => 'Dott.ssa Barbara Spica',
    'from'          => 'info@barbaraspica.it',     // deve essere = smtp_user
    'from_name'     => 'Dott.ssa Barbara Spica - Barbaraspica.it',

    // Anti-spam
    'min_fill_seconds' => 0,
    'rate_limit'    => 50,

    // Redirect
    'redirect_ok'   => '/contatti.html?inviato=1#form-status',
    'redirect_err'  => '/contatti.html?errore=',

    // Log
    'rate_log'      => __DIR__ . '/.contact-rate.log',
    'debug_log'     => __DIR__ . '/.contact-error.log',
    'debug'         => true,
];

// ============================================================
// LOGGING
// ============================================================
function logf($CONFIG, $msg) {
    @file_put_contents($CONFIG['debug_log'],
        date('Y-m-d H:i:s') . ' ' . $msg . "\n",
        FILE_APPEND);
}
function fail($CONFIG, $reason) {
    logf($CONFIG, 'FAIL ' . $reason);
    $code = $CONFIG['debug'] ? $reason : '1';
    header("Location: " . $CONFIG['redirect_err'] . urlencode($code) . '#form-status');
    exit;
}
function ok_redirect($CONFIG, $detail) {
    logf($CONFIG, 'OK ' . $detail);
    header("Location: " . $CONFIG['redirect_ok']);
    exit;
}
function clean($s) {
    return trim((string)$s);
}

// ============================================================
// SMTP CLIENT (minimal, no dependencies)
// ============================================================
function smtp_send($CONFIG, $to, $subject, $body_plain) {
    $host   = $CONFIG['smtp_host'];
    $port   = (int)$CONFIG['smtp_port'];
    $secure = strtolower($CONFIG['smtp_secure']);
    $user   = $CONFIG['smtp_user'];
    $pass   = $CONFIG['smtp_pass'];
    $from   = $CONFIG['from'];
    $fromN  = $CONFIG['from_name'];

    $remote = ($secure === 'ssl' ? 'ssl://' : '') . $host . ':' . $port;
    $sock = @stream_socket_client($remote, $errno, $errstr, 15,
        STREAM_CLIENT_CONNECT, stream_context_create([
            'ssl' => ['verify_peer' => false, 'verify_peer_name' => false]
        ]));
    if (!$sock) {
        return [false, "connect-failed: $errstr ($errno)"];
    }
    stream_set_timeout($sock, 15);

    $read = function () use ($sock) {
        $data = '';
        while (!feof($sock)) {
            $line = fgets($sock, 1024);
            if ($line === false) break;
            $data .= $line;
            // Multi-line response: "250-..." continues, "250 ..." ends
            if (isset($line[3]) && $line[3] === ' ') break;
        }
        return $data;
    };
    $write = function ($cmd) use ($sock) {
        fwrite($sock, $cmd . "\r\n");
    };
    $exec = function ($cmd, $expect) use ($read, $write) {
        $write($cmd);
        $resp = $read();
        $code = (int) substr(trim($resp), 0, 3);
        return [$code === $expect, $resp];
    };

    // Greeting
    $g = $read();
    if (strpos($g, '220') !== 0) return [false, 'no-greeting: ' . $g];

    // EHLO
    [$o, $r] = $exec('EHLO ' . ($_SERVER['HTTP_HOST'] ?? 'localhost'), 250);
    if (!$o) return [false, 'ehlo-failed: ' . $r];

    // STARTTLS se richiesto
    if ($secure === 'tls') {
        [$o, $r] = $exec('STARTTLS', 220);
        if (!$o) return [false, 'starttls-failed: ' . $r];
        if (!@stream_socket_enable_crypto($sock, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
            return [false, 'tls-handshake-failed'];
        }
        // Re-EHLO dopo TLS
        [$o, $r] = $exec('EHLO ' . ($_SERVER['HTTP_HOST'] ?? 'localhost'), 250);
        if (!$o) return [false, 'ehlo2-failed: ' . $r];
    }

    // AUTH LOGIN
    [$o, $r] = $exec('AUTH LOGIN', 334);
    if (!$o) return [false, 'auth-not-accepted: ' . $r];
    [$o, $r] = $exec(base64_encode($user), 334);
    if (!$o) return [false, 'auth-user-rejected: ' . $r];
    [$o, $r] = $exec(base64_encode($pass), 235);
    if (!$o) return [false, 'auth-pass-rejected: ' . $r];

    // MAIL FROM
    [$o, $r] = $exec("MAIL FROM:<$from>", 250);
    if (!$o) return [false, 'mail-from-rejected: ' . $r];

    // RCPT TO
    [$o, $r] = $exec("RCPT TO:<$to>", 250);
    if (!$o) return [false, 'rcpt-rejected: ' . $r];

    // DATA
    [$o, $r] = $exec('DATA', 354);
    if (!$o) return [false, 'data-not-accepted: ' . $r];

    // Message
    $msgid = sprintf('<%s.%s@%s>', uniqid(), bin2hex(random_bytes(4)), $host);
    $headers = [
        'Date: ' . date('r'),
        'Message-ID: ' . $msgid,
        'From: ' . $fromN . ' <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: barbaraspica.it',
    ];
    $data = implode("\r\n", $headers) . "\r\n\r\n" . $body_plain;
    // Dot-stuffing per evitare terminazione precoce
    $data = preg_replace('/(^|\r\n)\.(?=\r\n|$)/', '$1..', $data);
    $write($data . "\r\n.");
    $resp = $read();
    if (substr(trim($resp), 0, 3) !== '250') {
        return [false, 'data-rejected: ' . $resp];
    }

    // QUIT
    $write('QUIT');
    fclose($sock);
    return [true, 'sent ' . $msgid];
}

// ============================================================
// MAIN
// ============================================================
logf($CONFIG, '--- new submit method=' . $_SERVER['REQUEST_METHOD']);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail($CONFIG, 'method-not-post');
}
if (!empty($_POST['website'])) ok_redirect($CONFIG, 'honeypot');
if (($_POST['form_id'] ?? '') !== 'contact_v1') fail($CONFIG, 'bad-form-id');
if (empty($_POST['privacy'])) fail($CONFIG, 'no-privacy-consent');

$name    = clean($_POST['name'] ?? '');
$surname = clean($_POST['surname'] ?? '');
$email   = clean($_POST['email'] ?? '');
$phone   = clean($_POST['phone'] ?? '');
$subject = clean($_POST['subject'] ?? 'Informazioni generali');
$message = clean($_POST['message'] ?? '');

logf($CONFIG, "fields name='$name' email='$email' msg_len=" . mb_strlen($message));

if (mb_strlen($name) < 2 || mb_strlen($name) > 80) fail($CONFIG, 'invalid-name');
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 120) fail($CONFIG, 'invalid-email');
if (mb_strlen($message) < 10 || mb_strlen($message) > 3000) fail($CONFIG, 'invalid-message-length');

// Rate limit
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$count = 0;
if (is_file($CONFIG['rate_log'])) {
    foreach (file($CONFIG['rate_log'], FILE_IGNORE_NEW_LINES) as $line) {
        list($t, $i) = array_pad(explode("\t", $line, 2), 2, '');
        if ((int)$t > time() - 3600 && $i === $ip) $count++;
    }
}
if ($count >= $CONFIG['rate_limit']) fail($CONFIG, 'rate-limit');
@file_put_contents($CONFIG['rate_log'], time() . "\t" . $ip . "\n", FILE_APPEND);

// Verifica password configurata
if (strpos($CONFIG['smtp_pass'], 'INSERISCI') === 0) {
    fail($CONFIG, 'smtp-password-not-configured');
}

// Costruisci body
$display_name = trim("$name $surname");
$mail_subject = "[Dott.ssa Barbara Spica - Sito] $subject - da $display_name";

$body  = "Hai ricevuto un nuovo messaggio dal modulo di contatto del tuo sito.\r\n";
$body .= "================================================================\r\n\r\n";
$body .= "Nome:       $display_name\r\n";
$body .= "Email:      $email\r\n";
if ($phone) $body .= "Telefono:   $phone\r\n";
$body .= "Oggetto:    $subject\r\n";
$body .= "Data:       " . date('d/m/Y H:i') . "\r\n\r\n";
$body .= "----------------------------------------------------------------\r\n";
$body .= "Messaggio:\r\n\r\n";
$body .= $message . "\r\n\r\n";
$body .= "----------------------------------------------------------------\r\n";
$body .= "IP: $ip\r\n";

// Invio
[$ok, $detail] = smtp_send($CONFIG, $CONFIG['to'], $mail_subject, $body);
logf($CONFIG, 'main_send: ' . ($ok ? 'OK' : 'FAIL') . ' - ' . $detail);

if (!$ok) fail($CONFIG, 'smtp-' . substr(preg_replace('/[^a-z0-9-]/i','-', $detail), 0, 60));

// Auto-reply (best effort)
$auto_subject = "Ho ricevuto il tuo messaggio";
$auto_body  = "Ciao $name,\r\n\r\n";
$auto_body .= "ho ricevuto correttamente il tuo messaggio attraverso il sito.\r\n";
$auto_body .= "Ti ricontattero' il prima possibile (di norma entro 1-2 giorni lavorativi).\r\n\r\n";
$auto_body .= "Per richieste urgenti puoi chiamarmi al +39 349 7543276 o scrivermi su WhatsApp.\r\n\r\n";
$auto_body .= "Un caro saluto,\r\n";
$auto_body .= "Dott.ssa Barbara Spica\r\n";
$auto_body .= "TNPEE & Psicologa\r\n";
$auto_body .= "https://barbaraspica.it\r\n";

[$ok2, $detail2] = smtp_send($CONFIG, $email, $auto_subject, $auto_body);
logf($CONFIG, 'auto_reply: ' . ($ok2 ? 'OK' : 'FAIL') . ' - ' . $detail2);

ok_redirect($CONFIG, 'sent to ' . $CONFIG['to']);
