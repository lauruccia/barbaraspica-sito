<?php
/**
 * Form contatti - barbaraspica.it
 *
 * Riceve POST dal form di /contatti.html, valida i dati,
 * invia email a info@barbaraspica.it via mail() di PHP.
 *
 * Anti-spam:
 *  - Honeypot (campo nascosto "website")
 *  - Time-trap (form compilato in meno di 3 secondi = bot)
 *  - Rate limiting su file (max 5 invii/ora dallo stesso IP)
 *  - Validazione lato server di TUTTI i campi
 *
 * Privacy: nessun dato salvato su disco oltre al rate-limit log temporaneo.
 */

// ============================================================
// CONFIGURAZIONE
// ============================================================
$CONFIG = [
    // Indirizzo destinatario (modifica qui se cambia)
    'to'         => 'info@barbaraspica.it',
    'to_name'    => 'Dott.ssa Barbara Spica',

    // From: deve essere un indirizzo del DOMINIO che esiste come account email
    // sul tuo cPanel. Se "noreply@" non esiste o se l'hosting blocca, usa "info@".
    'from'       => 'info@barbaraspica.it',
    'from_name'  => 'Sito barbaraspica.it',

    // Reply-To verrà impostato automaticamente sull'email dell'utente

    // Min secondi che l'utente DEVE impiegare per compilare (anti-bot)
    'min_fill_seconds' => 3,

    // Max submission per IP per ora
    'rate_limit'  => 5,

    // Pagina dopo invio (con parametro success/error)
    'redirect_ok'  => '/contatti.html?inviato=1#form-status',
    'redirect_err' => '/contatti.html?errore=1#form-status',

    // Log temporaneo (per rate-limit) - va in cartella scrivibile
    'rate_log' => __DIR__ . '/.contact-rate.log',
];

// ============================================================
// FUNZIONI HELPER
// ============================================================

function clean($s) {
    return trim(filter_var($s, FILTER_UNSAFE_RAW, FILTER_FLAG_STRIP_LOW));
}

function bad_request($msg = 'Richiesta non valida') {
    http_response_code(400);
    header('Content-Type: text/plain; charset=utf-8');
    echo $msg;
    exit;
}

function redirect_with($url) {
    header("Location: $url");
    exit;
}

function check_rate_limit($ip, $cfg) {
    $log = $cfg['rate_log'];
    $now = time();
    $hour_ago = $now - 3600;
    $entries = [];
    if (is_file($log)) {
        foreach (file($log, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
            list($t, $i) = array_pad(explode("\t", $line, 2), 2, '');
            $t = (int)$t;
            if ($t > $hour_ago) {
                $entries[] = "$t\t$i";
            }
        }
    }
    $count_ip = 0;
    foreach ($entries as $e) {
        list(, $i) = explode("\t", $e);
        if ($i === $ip) $count_ip++;
    }
    if ($count_ip >= $cfg['rate_limit']) {
        return false;
    }
    $entries[] = "$now\t$ip";
    @file_put_contents($log, implode("\n", $entries));
    return true;
}

// ============================================================
// MAIN
// ============================================================

// Solo POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    bad_request('Metodo non consentito');
}

// Honeypot
if (!empty($_POST['website'])) {
    // Bot detected: silently pretend success
    redirect_with($CONFIG['redirect_ok']);
}

// Time trap
$start_ts = (int)($_POST['start_ts'] ?? 0);
$now = time();
if ($start_ts <= 0 || ($now - $start_ts) < $CONFIG['min_fill_seconds']) {
    redirect_with($CONFIG['redirect_ok']); // silent
}

// Form ID
if (($_POST['form_id'] ?? '') !== 'contact_v1') {
    bad_request('Form non riconosciuto');
}

// Privacy consent
if (empty($_POST['privacy'])) {
    redirect_with($CONFIG['redirect_err']);
}

// Validazione campi
$name    = clean($_POST['name'] ?? '');
$surname = clean($_POST['surname'] ?? '');
$email   = clean($_POST['email'] ?? '');
$phone   = clean($_POST['phone'] ?? '');
$subject = clean($_POST['subject'] ?? 'Informazioni generali');
$message = clean($_POST['message'] ?? '');

if (mb_strlen($name) < 2 || mb_strlen($name) > 80) {
    redirect_with($CONFIG['redirect_err']);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 120) {
    redirect_with($CONFIG['redirect_err']);
}
if (mb_strlen($message) < 10 || mb_strlen($message) > 3000) {
    redirect_with($CONFIG['redirect_err']);
}

// Rate limit
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
if (!check_rate_limit($ip, $CONFIG)) {
    redirect_with($CONFIG['redirect_err']);
}

// Costruzione email
$display_name = trim("$name $surname");
$mail_subject = "[Sito] $subject — da $display_name";
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';

$body  = "Hai ricevuto un nuovo messaggio dal modulo di contatto del tuo sito.\r\n";
$body .= "================================================================\r\n\r\n";
$body .= "Nome:       $display_name\r\n";
$body .= "Email:      $email\r\n";
if ($phone) $body .= "Telefono:   $phone\r\n";
$body .= "Oggetto:    $subject\r\n";
$body .= "Data:       " . date('d/m/Y H:i') . "\r\n";
$body .= "\r\n----------------------------------------------------------------\r\n";
$body .= "Messaggio:\r\n\r\n";
$body .= $message . "\r\n\r\n";
$body .= "----------------------------------------------------------------\r\n";
$body .= "Privacy: ✓ accettata\r\n";
$body .= "IP: $ip\r\n";
$body .= "Browser: $user_agent\r\n";

// Headers
$from_safe    = $CONFIG['from'];
$from_name    = $CONFIG['from_name'];
$reply_to     = $email;
$reply_name   = $display_name;

$headers  = "From: =?UTF-8?B?" . base64_encode($from_name) . "?= <$from_safe>\r\n";
$headers .= "Reply-To: =?UTF-8?B?" . base64_encode($reply_name) . "?= <$reply_to>\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

$subj_b64 = "=?UTF-8?B?" . base64_encode($mail_subject) . "?=";

// Verifica se mail() esiste/è abilitata
if (!function_exists('mail')) {
    @file_put_contents(__DIR__.'/.contact-error.log',
        date('Y-m-d H:i:s')." mail() disabled\n", FILE_APPEND);
    redirect_with($CONFIG['redirect_err']);
}

// Invio email principale a info@barbaraspica.it
$ok = @mail($CONFIG['to'], $subj_b64, $body, $headers, "-f " . $from_safe);

// Se fallisce, prova senza il -f (alcuni hosting non lo accettano)
if (!$ok) {
    $ok = @mail($CONFIG['to'], $subj_b64, $body, $headers);
}

// Log dell'esito (per debug, visibile solo via FileManager)
@file_put_contents(__DIR__.'/.contact-error.log',
    date('Y-m-d H:i:s')." mail()=" . ($ok ? "OK" : "FAIL") . " to={$CONFIG['to']} from=$from_safe\n",
    FILE_APPEND);

// Auto-reply all'utente (se mail() ha funzionato)
if ($ok) {
    $auto_subject = "Ho ricevuto il tuo messaggio";
    $auto_body  = "Ciao $name,\r\n\r\n";
    $auto_body .= "ho ricevuto correttamente il tuo messaggio attraverso il sito.\r\n";
    $auto_body .= "Ti ricontatterò il prima possibile (di norma entro 1-2 giorni lavorativi).\r\n\r\n";
    $auto_body .= "Per richieste urgenti puoi chiamarmi al " . "+39 349 7543276" . " o scrivermi su WhatsApp.\r\n\r\n";
    $auto_body .= "Un caro saluto,\r\n";
    $auto_body .= "Dott.ssa Barbara Spica\r\n";
    $auto_body .= "TNPEE & Psicologa\r\n";
    $auto_body .= "https://barbaraspica.it\r\n";

    $auto_headers  = "From: =?UTF-8?B?" . base64_encode("Dott.ssa Barbara Spica") . "?= <" . $CONFIG['to'] . ">\r\n";
    $auto_headers .= "MIME-Version: 1.0\r\n";
    $auto_headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    @mail($email, "=?UTF-8?B?" . base64_encode($auto_subject) . "?=", $auto_body, $auto_headers);
}

// Redirect finale
redirect_with($ok ? $CONFIG['redirect_ok'] : $CONFIG['redirect_err']);
