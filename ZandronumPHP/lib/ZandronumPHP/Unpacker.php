<?php

namespace ZandronumPHP;

class Unpacker
{
  private $binaryString;
  private $position;

  public function __construct($binaryString)
  {
    $this->binaryString = $binaryString;
    $this->position = 0;
  }

  public function readBytes($count)
  {
    $ret = substr($this->binaryString, $this->position, $count);
    $this->position += $count;
    return $ret;
  }

  public function readByte()
  {
    return $this->readBytes(1);
  }

  public function readByteBool()
  {
    return (bool)(ord($this->readBytes(1)));
  }

  public function readByteNum()
  {
    return ord($this->readBytes(1));
  }

  public function readLong()
  {
    return unpack('V', $this->readBytes(4))[1];
  }

  public function readShort()
  {
    return unpack('v', $this->readBytes(2))[1];
  }

  public function readFloat()
  {
    return unpack('f', $this->readBytes(4))[1];
  }

  public function readString()
  {
    $string = '';
    while (($byte = ord($this->readByte())) != 0)
    {
      $string .= chr($byte);
    }
    return $string;
  }

  public function getLastByteNum()
  {
    return ord(substr($this->binaryString, -1));
  }

}

