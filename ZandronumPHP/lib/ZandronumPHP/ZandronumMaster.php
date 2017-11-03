<?php

namespace ZandronumPHP;

require_once(__DIR__ . '/MasterRequest.php');
require_once(__DIR__ . '/MasterResponse.php');

class ZandronumMaster
{
  private $decoded;

  public function __construct()
  {
    $payload = pack("V", MasterRequest::CHALLENGE) . pack("v", MasterRequest::VERSION);

    $connection = new Connection("master.zandronum.com", 15300);
    $connection->send($payload);
    $this->decoded = "";
    do
    {
      $received = $connection->receive();
      $this->decoded .= $received;
      $unpacker = new Unpacker($received);
      $lastbyte = $unpacker->getLastByteNum();
    }
    while ($lastbyte == MasterResponse::END_SERVER_LIST_PART);
  }

  public function getData()
  {
    $data = null;
    if ($this->decoded)
    {
      $data = new \stdClass();
      $data->servers = array();
      $unpacker = new Unpacker($this->decoded);

      while(true)
      {
        $response = $unpacker->readLong();
        if ($response != MasterResponse::BEGIN_SERVER_LIST_PART)
          break;

        $packetnumber = $unpacker->readByteNum();
        while(true)
        {
          $command = $unpacker->readByteNum();
          if ($command == MasterResponse::BEGIN_SERVER_BLOCK)
          {
            while ($block_byte = $unpacker->readByteNum())
            {
              if ($block_byte == MasterResponse::END_SERVER_BLOCK) break 1;
              $ports = $block_byte;
              for ($i = 0; $i < 4; $i++) $octets[$i] = $unpacker->readByteNum();
              $ip = implode(".", $octets);
              for ($i = 0; $i < $ports; $i++)
              {
                $port = $unpacker->readShort();
                array_push($data->servers, $ip . ":" . $port);
              }
            }
          }
          else if ($command == MasterResponse::END_SERVER_LIST_PART) break 1;
          else if ($command == MasterResponse::END_SERVER_LIST) return $data;
        }
      }
    }
  }

}
