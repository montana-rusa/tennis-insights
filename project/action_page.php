$player = $_POST['fname'] ?? '';

echo file_get_contents(
    'http://localhost:5000/', 
    false, 
    stream_context_create([
        'http' => [
            'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
            'method'  => 'POST',
            'content' => http_build_query(['fname' => $player])
        ]
    ])
);