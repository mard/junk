<?php

namespace ZandronumPHP;

class Connection
{
  private $socket;
  private $host;
  private $port;

  public function __construct($host, $port)
  {
    $this->socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
    $this->host = $host;
    $this->port = intval($port);
  }

  public function send($payload, $timeout = GameRequest::DEFAULT_TIMEOUT)
  {
    socket_set_option($this->socket, SOL_SOCKET, SO_SNDTIMEO, array('sec'=>floor($timeout/1000),'usec'=>$timeout%1000));
    $payload_compressed = Huffman::encode($payload);

    socket_connect($this->socket, $this->host, $this->port);
    socket_send($this->socket, $payload_compressed, strlen($payload_compressed), 0);
  }

  public function receive($timeout = GameResponse::DEFAULT_TIMEOUT)
  {
    socket_set_option($this->socket, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>floor($timeout/1000),'usec'=>$timeout%1000));
    $response = "";
    if (false !== ($bytes = socket_recv($this->socket, $response, 4096, 0)))
    {
      return Huffman::decode($response);
    }
    else
    {
      echo "socket_recv() failed; reason: " . socket_strerror(socket_last_error($this->socket)) . "\n";
      return false;
    }
  }

}

