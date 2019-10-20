const pluginName = 'ConvertTxtToJsonPlugin';
const { SyncHook } = require('tapable');
const fs = require('fs');
const path = require("path");

class ConvertTxtToJsonPlugin {
  constructor(options) {
    console.log('@plugin constructor', options);
  }

  apply(compiler) {
    compiler.hooks.myPlugin = new SyncHook(['data']);

    compiler.hooks.beforeCompile.tap(pluginName, (compilationParams) => {
      if (!fs.existsSync(path.resolve("./dist")))
        fs.mkdirSync(path.resolve("./dist"));
      const pathAssets = path.join(__dirname, "assets");
      var entriesAssets = [];
      fs.readdirSync(pathAssets)
        .forEach(file => entriesAssets.push(path.resolve("./" + path.join("assets", file))));
      entriesAssets
        .forEach(file => {
          var somefile = getFileContents(file);
          var txtToSave = convertTxtToJson(somefile);
          putFileContents(path.resolve("./" + path.join("dist", path.basename(file, '.txt') + '.json')), txtToSave);
        });
    });
  }
}

function convertTxtToJson(input) {
  var array = input.replace(/\r?\n|\r/g, ";").trim(';').split(";").sort();
  return JSON.stringify(array, null, 2);
}

function getFileContents(path) {
  return fs.readFileSync(path, 'utf8');
}

function putFileContents(path, input) {
  fs.writeFileSync(path, input);
}

module.exports = ConvertTxtToJsonPlugin;