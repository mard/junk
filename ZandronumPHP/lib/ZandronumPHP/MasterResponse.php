<?php

namespace ZandronumPHP;

class MasterResponse
{
  const BANNED                 = 3;
  const IGNORED                = 4;
  const WRONGVER               = 5;
  const BEGIN_SERVER_LIST_PART = 6;
  const BEGIN_SERVER_BLOCK     = 8;
  const END_SERVER_BLOCK       = 0;
  const END_SERVER_LIST        = 2;
  const END_SERVER_LIST_PART   = 7;
}
