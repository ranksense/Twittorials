const { fetchTable, addToTable } = require('./sqlTables');

const dbPath = '../databaseName.db'; // Adapt

const tableName = `"tableName"`; // Adapt

async function addOriginalUrlsToDB(dbPath, tableName) {
  const urls = await fetchTable(dbPath, tableName);

  const urlMapping = urls.map(url => {
    const { Address: volatileURL } = url;
    const originalURL = 
    volatileURL
      .replace('volatile-url-to-replace', '') // Adapt
      .replace('http://', 'https://') // Adapt
    return { volatileURL, originalURL }
  })

  await addToTable(dbPath, urlMapping, tableName)
}

addOriginalUrlsToDB(dbPath, tableName)