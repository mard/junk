<?php
require_once(__DIR__ . '/../vendor/autoload.php');

use ZandronumPHP\Cache;
use ZandronumPHP\ZandronumGame;
use ZandronumPHP\GameRequestFlags;
use ZandronumPHP\GameResponse;

if (isset($_GET['remote']))
{
  $remote = explode(":", $_GET['remote']);
  $host = $remote[0];
  $port = @$remote[1];
  if (!$port) $port = 10666;
  $request_flag = GameRequestFlags::all();
  $cache_path = __DIR__ . DIRECTORY_SEPARATOR . 'cache.txt';
  $cache = is_writable(dirname($cache_path)) ? new Cache($cache_path) : null;
  $zg = new ZandronumGame($host, $port, $request_flag, $cache);
  $zd = $zg->get();
}

?>

<form action="<?php $_PHP_SELF ?>" method="GET">
<p><input type="text" name="remote" placeholder="example.com:10666" value="<?php if (isset($_GET['remote'])) echo $_GET['remote']; ?>"/><input type="submit" /></p>
</form>

<?php if (isset($zd)): ?>
  <p>Server query time: <?php echo date('c', $zd['servertime']); ?><br/>Real query time: <?php echo date('c', $zd['realtime']); ?></p>
  <?php if ($zd['response'] == GameResponse::IGNORED): ?>
    <p>Your request have been rejected because you tried to refresh too soon. Please wait few more seconds and try again.</p>
  <?php elseif ($zd['response'] == GameResponse::BANNED): ?>
    <p>Your IP is banned on this server.</p>
  <?php elseif ($zd['response'] == GameResponse::OK): ?>
    <h1><?php echo $zd['name']; ?>.</h1>
    <p><?php echo $zd['version']; ?></p>
    <p>Cached: <?php echo $zd['cached']; ?></p>

    <ul>
      <li>URL: <a href="<?php echo $zd['url']; ?>"><?php echo $zd['url']; ?></a></li>
      <li>Email: <?php echo $zd['email']; ?></li>
    </ul>

    <ul>
      <li>Request flags: <?php echo $zd['flags']; ?></li>
      <li>MD5 sum: <?php echo $zd['md5sum']; ?></li>
      <li>IWAD: <?php echo $zd['iwad']; ?></li>
      <li>PWADs: <?php echo $zd['pwads_count']; ?>
        <ul>
        <?php foreach ($zd['pwads'] as $pwad): ?>
          <li><?php echo $pwad; ?></li>
        <?php endforeach; ?>
        </ul>
      </li>
      <li>Force password: <?php echo $zd['forcepassword']; ?></li>
      <li>Force join password: <?php echo $zd['forcejoinpassword']; ?></li>
      <li>Testing server: <?php echo $zd['testingserver']; ?></li>
      <li>Testing server name: <?php echo $zd['testingservername']; ?></li>
      <li>Flags: <?php echo $zd['flagcount']; ?>
        <ul>
          <?php foreach ($zd['dmflags'] as $flag): ?>
            <li><?php echo $flag; ?></li>
          <?php endforeach; ?>
        </ul>
      </li>
      <li>Security settings: <?php echo $zd['securitysettings']; ?></li>
      <li>Testing server name: <?php echo $zd['testingservername']; ?></li>
    </ul>

    <ul>
      <li>Players: <?php echo $zd['numplayers']; ?>/<?php echo $zd['maxplayers']; ?>/<?php echo $zd['maxclients']; ?> (clients/maxplayers/maxclients)</li>
      <li>Game name: <?php echo $zd['gamename']; ?></li>
      <li>Current map: <?php echo $zd['mapname']; ?></li>
      <li>Gamemode: <?php echo $zd['gamemode']; ?></li>
      <li>Teamgame: <?php echo $zd['playersonteams']; ?></li>
      <li>Instagib: <?php echo $zd['instagib']; ?></li>
      <li>Buckshot: <?php echo $zd['buckshot']; ?></li>
      <li>Gameskill: <?php echo $zd['gameskill']; ?></li>
      <li>Botskill: <?php echo $zd['botskill']; ?></li>
      <li>Fraglimit: <?php echo $zd['fraglimit']; ?></li>
      <li>Timelimit: <?php echo $zd['timelimit']; ?></li>
      <li>Duellimit: <?php echo $zd['duellimit']; ?></li>
      <li>Pointlimit: <?php echo $zd['pointlimit']; ?></li>
      <li>Winlimit: <?php echo $zd['winlimit']; ?></li>
    </ul>

    <?php if ($zd['numplayers'] > 0): ?>
      <h2>Players</h2>
      <table>
        <tr>
          <th>Name</th>
          <th>Score</th>
          <?php if($zd['playersonteams']): ?>
            <th>Team</th>
          <?php endif; ?>
          <th>Ping</th>
          <th>Time (minutes)</th>
          <th>Spectator</th>
          <th>Bot</th>
        </tr>

        <?php usort($zd['players'], function($a, $b) { return $b['score'] - $a['score']; }); ?>
        <?php foreach ($zd['players'] as $player): ?>
          <tr>
            <td><?php echo $zg->colorizeSpan($player['name'], $player['color_positions']); ?></td>
            <td><?php echo $player['score'];?></td>
            <?php if($zd['playersonteams']): ?>
              <td><?php echo $player['team'];?></td>
            <?php endif; ?>
            <td><?php echo $player['ping'];?></td>
            <td><?php echo $player['time'];?></td>
            <td><?php echo $player['spectator'];?></td>
            <td><?php echo $player['bot'];?></td>
          </tr>
        <?php endforeach; ?>
      </table>
    <?php endif; ?>

    <?php if($zd['playersonteams']): ?>
      <h2>Teams</h2>
      <table>
        <tr><th>Name</th><th>Color</th><th>Score</th></tr>
        <?php foreach ($zd['teaminfo'] as $teaminfo): ?>
          <tr>
            <td><?php echo $teaminfo['name']; ?></td>
            <td><?php echo $teaminfo['color']; ?></td>
            <td><?php echo $teaminfo['score']; ?></td>
          </tr>
        <?php endforeach; ?>
      </table>
    <?php endif; ?>

  <?php else: ?>
    <p>Unknown game response: <?php var_dump($zd['response']) ?></p>
  <?php endif; ?>
<?php endif; ?>
