<html>
<body>
<? $j = fopen("index.cgi","r");
   while(!feof($j)){
     fread($j,buf,65536);
     print buf;
   }
?>
</body>
