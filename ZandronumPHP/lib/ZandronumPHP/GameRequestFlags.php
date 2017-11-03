<?php

namespace ZandronumPHP;

class GameRequestFlags
{
  const NAME              = 0x00000001;
  const URL               = 0x00000002;
  const EMAIL             = 0x00000004;
  const MAPNAME           = 0x00000008;
  const MAXCLIENTS        = 0x00000010;
  const MAXPLAYERS        = 0x00000020;
  const PWADS             = 0x00000040;
  const GAMETYPE          = 0x00000080;
  const GAMENAME          = 0x00000100;
  const IWAD              = 0x00000200;
  const FORCEPASSWORD     = 0x00000400;
  const FORCEJOINPASSWORD = 0x00000800;
  const GAMESKILL         = 0x00001000;
  const BOTSKILL          = 0x00002000;
  const DMFLAGS           = 0x00004000; // deprecated
  const LIMITS            = 0x00010000;
  const TEAMDAMAGE        = 0x00020000;
  const TEAMSCORES        = 0x00040000; // deprecated
  const NUMPLAYERS        = 0x00080000;
  const PLAYERDATA        = 0x00100000;
  const TEAMINFO_NUMBER   = 0x00200000;
  const TEAMINFO_NAME     = 0x00400000;
  const TEAMINFO_COLOR    = 0x00800000;
  const TEAMINFO_SCORE    = 0x01000000;
  const TESTING_SERVER    = 0x02000000;
  const DATA_MD5SUM       = 0x04000000;
  const ALL_DMFLAGS       = 0x08000000;
  const SECURITY_SETTINGS = 0x10000000;

  public static function all()
  {
    $refl = new \ReflectionClass(get_called_class());
    $flags = 0;
    foreach (array_values($refl->getConstants()) as $value)
      $flags |= $value;
    return $flags;
  }
};
