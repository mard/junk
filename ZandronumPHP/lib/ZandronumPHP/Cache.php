<?php

namespace ZandronumPHP;

class Cache
{
  private $path;

  public function __construct($path)
  {
    $this->path = $path;
  }

  public function load()
  {
    $loaded = unserialize(file_get_contents($this->path));
    return $loaded;
  }

  public function save($parsed_data)
  {
    $parsed_data['cached'] = true;
    file_put_contents($this->path, serialize($parsed_data));
  }

  public function exists()
  {
    return file_exists($this->path);
  }

  public function expiredExpected()
  {
    if ($this->exists())
    {
      $loaded = unserialize(file_get_contents($this->path));
      return (time() - $loaded['realtime'] > 10);
    }
    return true;
  }
}
