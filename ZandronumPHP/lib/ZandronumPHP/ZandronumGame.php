<?php

namespace ZandronumPHP;

require_once(__DIR__ . '/GameModes.php');
require_once(__DIR__ . '/GameRequest.php');
require_once(__DIR__ . '/GameResponse.php');
require_once(__DIR__ . '/GameRequestFlags.php');

class ZandronumGame
{
  const ESCAPE_COLOR_CHAR = 034;

  public $host;
  public $port;
  public $request_flags;
  private $cache;

  public function __construct($host, $port, $request_flags = GameRequest::DEFAULT_REQUEST_FLAGS, $cache = null)
  {
    $this->host = $host;
    $this->port = $port;
    $this->request_flags = $request_flags;
    $this->cache = $cache;
  }

  public function get()
  {
    if ($this->cache && $this->cache->exists() && !$this->cache->expiredExpected())
      return $this->acquireFromCache();

    $p = $this->acquireFromInternet();

    if ($p['response'] != GameResponse::OK)
    {
      if ($this->cache && $this->cache->exists())
        return $this->acquireFromCache();
      return $p;
    }
    else if ($this->cache)
    {
      $this->cache->save($p);
    }

    return $p;
  }

  public function colorizeSpan($clean_name, $color_positions)
  {
    $ret = "";
    $colored = false;
    for ($i = 0; $i <= strlen($clean_name); $i++)
    {
      if (isset($color_positions[$i]))
      {
        if ($color_positions[$i] != -1)
        {
          if ($colored)
          {
            $ret .= "</span>";
            $colored = false;
          }
          $ret .= "<span style=\"color:#" . $color_positions[$i] . "\">";
          $colored = true;
        }
        else if ($colored)
        {
          $ret .= "</span>";
          $colored = false;
        }
      }
      if (isset($clean_name[$i])) $ret .= $clean_name[$i];
    }
    return $ret;
  }

  private function acquireFromInternet()
  {
    if ($this->request_flags & GameRequestFlags::PLAYERDATA)
      $this->request_flags |= GameRequestFlags::NUMPLAYERS | GameRequestFlags::GAMETYPE;

    if ($this->request_flags & GameRequestFlags::TEAMSCORES ||
        $this->request_flags & GameRequestFlags::TEAMINFO_NAME ||
        $this->request_flags & GameRequestFlags::TEAMINFO_COLOR ||
        $this->request_flags & GameRequestFlags::TEAMINFO_SCORE)
      $this->request_flags |= GameRequestFlags::TEAMINFO_NUMBER;

    $payload = pack("V", GameRequest::CHALLENGE) . pack("V", $this->request_flags) . pack("V", time());

    $connection = new Connection($this->host, $this->port);
    $connection->send($payload);
    $parsed = $this->parse($connection->receive());
    $parsed['cached'] = false;
    $parsed['realtime'] = time();
    return $parsed;
  }

  private function acquireFromCache()
  {
    if (!$this->cache)
      throw new \Exception('No cache available!');
    return $this->cache->load();
  }

  private function parse($response)
  {
    if (!$response)
      return null;

    $unpacker = new Unpacker($response);

    $data = array();
    $data['response'] = $unpacker->readLong();
    $data['servertime'] = $unpacker->readLong();
    if ($data['response'] != GameResponse::OK)
      return $data;

    $data['version'] = $unpacker->readString();
    $data['flags'] = $unpacker->readLong();

    if ($data['flags'] & GameRequestFlags::NAME) $data['name'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::URL) $data['url'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::EMAIL) $data['email'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::MAPNAME) $data['mapname'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::MAXCLIENTS) $data['maxclients'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::MAXPLAYERS) $data['maxplayers'] = $unpacker->readByteNum();

    if ($data['flags'] & GameRequestFlags::PWADS)
    {
      $data['pwads_count'] = $unpacker->readByteNum();
      for ($i = 0; $i < $data['pwads_count']; $i++)
      {
        $data['pwads'][$i] = $unpacker->readString();
      }
    }

    if ($data['flags'] & GameRequestFlags::GAMETYPE)
    {
      $data['gamemode'] = $unpacker->readByteNum();
      $data['playersonteams'] = in_array($data['gamemode'], GameModes::teamGameModes());
      $data['instagib'] = $unpacker->readByteBool();
      $data['buckshot'] = $unpacker->readByteBool();
    }

    if ($data['flags'] & GameRequestFlags::GAMENAME) $data['gamename'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::IWAD) $data['iwad'] = $unpacker->readString();
    if ($data['flags'] & GameRequestFlags::FORCEPASSWORD) $data['forcepassword'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::FORCEJOINPASSWORD) $data['forcejoinpassword'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::GAMESKILL) $data['gameskill'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::BOTSKILL) $data['botskill'] = $unpacker->readByteNum();

    if ($data['flags'] & GameRequestFlags::DMFLAGS)
    {
      $data['dmflags_deprecated'] = $unpacker->readLong();
      $data['dmflags2_deprecated'] = $unpacker->readLong();
      $data['compatflags_deprecated'] = $unpacker->readLong();
    }

    if ($data['flags'] & GameRequestFlags::LIMITS)
    {
      $data['fraglimit'] = $unpacker->readShort();
      $data['timelimit'] = $unpacker->readShort();
      if ($data['timelimit'] > 0)
        $data['timeleft'] = $unpacker->readShort();
      $data['duellimit'] = $unpacker->readShort();
      $data['pointlimit'] = $unpacker->readShort();
      $data['winlimit'] = $unpacker->readShort();
    }

    if ($data['flags'] & GameRequestFlags::TEAMDAMAGE)
      $unpacker->readFloat();
    if ($data['flags'] & GameRequestFlags::TEAMSCORES)
    {
      $data['teamscores'][0] = $unpacker->readShort();
      $data['teamscores'][1] = $unpacker->readShort();
    }

    if ($data['flags'] & GameRequestFlags::NUMPLAYERS)
      $data['numplayers'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::PLAYERDATA && $data['flags'] & GameRequestFlags::NUMPLAYERS && $data['numplayers'] > 0)
    {
      for ($i = 0; $i < $data['numplayers']; $i++)
      {
        $data['players'][$i] = $this->parsePlayerName($unpacker->readString());
        $data['players'][$i]['score'] = $unpacker->readShort();
        $data['players'][$i]['ping'] = $unpacker->readShort();
        $data['players'][$i]['spectator'] = $unpacker->readByteBool();
        $data['players'][$i]['bot'] = $unpacker->readByteBool();
        if ($data['playersonteams'])
          $data['players'][$i]['team'] = $unpacker->readByteNum();
        $data['players'][$i]['time'] = $unpacker->readByteNum();
      }
    }

    if ($data['flags'] & GameRequestFlags::TEAMINFO_NUMBER)
      $data['teamcount'] = $unpacker->readByteNum();
    if ($data['flags'] & GameRequestFlags::TEAMINFO_NUMBER && $data['teamcount'] > 0)
    {
      if ($data['flags'] & GameRequestFlags::TEAMINFO_NAME)
        for ($i = 0; $i < $data['teamcount']; $i++)
          $data['teaminfo'][$i]['name'] = $unpacker->readString();
      if ($data['flags'] & GameRequestFlags::TEAMINFO_COLOR)
        for ($i = 0; $i < $data['teamcount']; $i++)
          $data['teaminfo'][$i]['color'] = $unpacker->readLong();
      if ($data['flags'] & GameRequestFlags::TEAMINFO_SCORE)
        for ($i = 0; $i < $data['teamcount']; $i++)
          $data['teaminfo'][$i]['score'] = $unpacker->readShort();
    }

    if ($data['flags'] & GameRequestFlags::TESTING_SERVER)
    {
      $data['testingserver'] = $unpacker->readByteBool();
      $data['testingservername'] = $unpacker->readString();
    }

    if ($data['flags'] & GameRequestFlags::DATA_MD5SUM)
      $data['md5sum'] = $unpacker->readString();

    $data['dmflags'] = array();
    if ($data['flags'] & GameRequestFlags::ALL_DMFLAGS)
    {
      $data['flagcount'] = $unpacker->readByteNum();
      for ($i = 0; $i < $data['flagcount']; $i++)
        $data['dmflags'][$i] = $unpacker->readLong();
    }

    if ($data['flags'] & GameRequestFlags::SECURITY_SETTINGS)
      $data['securitysettings'] = $unpacker->readByteNum();

    return $data;
  }

  private function parsePlayerName($name)
  {
    $colorchart = $this->getColorChart();
    $str = "";
    $clean_name = "";
    $color_positions = array();
    $colored = false;

    for ($i = 0; $i < strlen($name); $i++)
      if ((ord($name[$i]) >= 32 && ord($name[$i]) <= 126) || ord($name[$i]) == self::ESCAPE_COLOR_CHAR)
        $str .= $name[$i];

    for ($i = 0; $i < strlen($str); $i++)
    {
      if (ord($str[$i]) == self::ESCAPE_COLOR_CHAR)
      {
        $i++;
        if ($i >= strlen($str)) break;
        $colorchar = strtolower($str[$i]);
        $color = ord($colorchar) - 97;

        if ($colorchar == '+')
          $color = $current == 0 ? 19 : $current-1;
        else if ($colorchar == '*') $colorchar = 'd';
        else if ($colorchar == '!') $colorchar = 'q';
        else if ($colorchar == '[')
        {
          $end = strpos($str, ']', $i);
          if (!$end) break;
          $colorname = substr($str, $i+1, $end-$i-1);

          // NewTextColours1_170.pk3
          if (strlen($colorname) == 2)
            $color_positions[strlen($clean_name)] = $colorchart[strtoupper($colorname)];

          // named colours
          else if (!strpos($colorname, '"'))
            $color_positions[strlen($clean_name)] = $colorname;

          $i += strlen($colorname) + 1;
          $colored = true;
          continue;
        }
        else if ($colorchar == '-')
        {
          if ($colored)
            $color_positions[strlen($clean_name)] = -1;
          $colored = false;
          continue;
        }
        if ($colored)
        {
          $color_positions[strlen($clean_name)] = -1;
          $colored = false;
        }
        if($color >= 0 && $color < 22)
        {
          $color_positions[strlen($clean_name)] = $colorchart[$colorchar];
          $colored = true;
        }
        continue;
      }
      $clean_name .= $str[$i];
    }
    if($colored) $color_positions[strlen($clean_name)] = -1;
    return array("name" => $clean_name, "color_positions" => $color_positions);
  }

  private function getColorChart()
  {
    $chart = [];
    $contents = file_get_contents(__DIR__ . DIRECTORY_SEPARATOR . 'color_chart.txt');
    foreach (explode("\n", str_replace("\r", '', $contents)) as $line)
    {
      if (empty($line))
        continue;
      list ($key, $value) = preg_split('/\s+/', $line);
      $chart[$key] = $value;
    }
    return $chart;
  }

}

