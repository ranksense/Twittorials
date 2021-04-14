// Phillip Obosi - https://scotch.io/courses/the-ultimate-guide-to-javascript-algorithms/array-chunking

export const chunkArray = (array, size) => {
  let result = []
  for (let i = 0; i < array.length; i += size) {
    let chunk = array.slice(i, i + size)
    result.push(chunk)
  }
  return result
}
