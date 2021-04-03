const { connect, get, all, close, run } = require('./db');

async function fetchTable(dbPath, tableName) {
  let rows;
  
  const db = await connect(dbPath);

  try {
    rows = await all.call(db, `SELECT Address FROM ${tableName}`,[]);
  } catch(err) {
    console.log(err);
  } finally {
    await close.call(db);
  }

  return rows;
}

async function addToTable(dbPath, urlMapping, tableName) {
  const column =  'canonURL';

  const db = await connect(dbPath);

  try {
    
    if(! await columnExists(db, column, tableName)){
      await run.call(db,`ALTER TABLE ${tableName} ADD canonURL TEXT`);
    }
    
    urlMapping.map(async urlMap => {
      const { volatileURL, originalURL } = urlMap;
      await run.call(db,`UPDATE ${tableName} SET canonURL = ? WHERE Address = ?`, [originalURL, volatileURL])
    })
  } catch(err) {
    console.log(err);
  } finally {
    await close.call(db);
  }

}

async function columnExists(db, column, tableName) {
  let rows;
  
  try {
    rows = await get.call(db,`SELECT ${column} FROM ${tableName}`)
  } catch(err) {
    rows = null;
  } 
  return Boolean(rows);
}

module.exports = {
  fetchTable,
  addToTable
}