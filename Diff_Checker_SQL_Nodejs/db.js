const { promisify } = require('util');
const { Database } = require('sqlite3');

// Promisify all
const connect = promisify((path, cb) => new Database(path, function (err) { cb(err, this); }));
const get = promisify(Database.prototype.get);
const all = promisify(Database.prototype.all);
const run = promisify(Database.prototype.run);
const close = promisify(Database.prototype.close);

module.exports = {
  connect,
  get,
  all,
  run,
  close
}