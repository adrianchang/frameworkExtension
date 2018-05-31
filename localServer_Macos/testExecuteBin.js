var exec = require('child_process').exec;
exec("mas list", function(error, stdout, stderr) { console.log(stdout) });
// var exec  = require('child_process').exec,
//     child;

// child = exec('mas',
//   function (error, stdout, stderr) {
//     console.log('stdout:', stdout);
//     console.log('stderr:', stderr);
//     if (error !== null) {
//       console.log('exec error:', error);
//     }
// });