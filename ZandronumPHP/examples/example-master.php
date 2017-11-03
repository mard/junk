<?php
require_once(__DIR__ . '/../vendor/autoload.php');

use ZandronumPHP\ZandronumMaster;
//use ZandronumPHP\ZandronumGame;
//use ZandronumPHP\GameRequestFlags;

$zm = new ZandronumMaster();
$zd = $zm->getData();

?>

<?php if (isset($zm)): ?>
  <h1>Server list</h1>
  <table>
    <tr><th>ip:port</th><th>name</th></tr>
    <?php foreach ($zd->servers as $server): ?>
    <?php
      $remote = explode(":", $server);
      $host = $remote[0];
      $port = $remote[1];
      //$request_flag = GameRequestFlags::NAME;
      //$zg = new ZandronumGame($host, $port, $request_flag);
      //$zd = $zg->getData();
    ?>
      <tr><td><?php echo $server; ?></td><td><?php //echo $zd->name; ?></td></tr>
    <?php endforeach; ?>
  </table>
<?php endif; ?>
