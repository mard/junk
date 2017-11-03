<?php

namespace ZandronumPHP;

class GameModes
{
  const COOPERATIVE     = 0;
  const SURVIVAL        = 1;
  const INVASION        = 2;
  const DEATHMATCH      = 3;
  const TEAMPLAY        = 4;
  const DUEL            = 5;
  const TERMINATOR      = 6;
  const LASTMANSTANDING = 7;
  const TEAMLMS         = 8;
  const POSSESSION      = 9;
  const TEAMPOSSESSION  = 10;
  const TEAMGAME        = 11;
  const CTF             = 12;
  const ONEFLAGCTF      = 13;
  const SKULLTAG        = 14;
  const DOMINATION      = 15;

  // Returns gamemodes with GMF_PLAYERSONTEAMS flag set in gamemode.cpp.
  public static function teamGameModes()
  {
    return
    [
      self::TEAMPLAY,
      self::TEAMLMS,
      self::TEAMPOSSESSION,
      self::TEAMGAME,
      self::CTF,
      self::ONEFLAGCTF,
      self::SKULLTAG,
      self::DOMINATION
    ];
  }
}
