console.time()
/* Modules */
import fs from 'fs' // Access to File System
import csv from 'csvtojson' // Module to convert CSV into JSON
import axios from 'axios' // Module to make HTTP requests
import { parse } from 'json2csv' // Module to convert JSON into CSV
import moment from 'moment' // Module to interact with Date objects

/* Variables */
const file = 'urls.csv'
const folder = 'results'

////////* Custom Functions *////////

// Create HTTP request to API
const apiRequest = async (url) => {
  // API Parameters
  const endpoint = 'https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed' // Endpoint
  const key = '' // API Key
  const device = 'mobile' // Test viewport. 'desktop' also available

  const response = await axios(`${endpoint}?url=${url}&strategy=${device}&key=${key}`)
  return response.data
}

////////* Start of script *////////

// Create results folder
if (fs.existsSync(`./${folder}`)) {
  console.log('Results folder exists')
} else {
  console.log('Creating results folder')
  fs.mkdir(`./${folder}`, (err) => {
    if (err) console.log('Error creating folder')
  })
}

// Extract URLs from file
const getUrls = async () => {
  const list = await csv().fromFile(file)
  return list.map(({ url }) => url)
}

// Function to extract CruX data from API
const getFieldData = async () => {
  const fieldDataRes = []
  const fieldOriginRes = []
  const urlList = await getUrls()

  // Loop through file items
  for (const url of urlList) {
    // Store response
    console.log(`Requesting Field data for ${url}...`)
    const result = await apiRequest(url)
    const fieldMetrics = result.loadingExperience.metrics
    const originFallback = result.loadingExperience.origin_fallback

    // If there is no field data break the loop
    if (!fieldMetrics) {
      console.log(`No Field data exists for ${url}`)
    } else {
      if (!originFallback) {
        // Otherwise Extract Field metrics (if there are)
        const fieldFCP = fieldMetrics.FIRST_CONTENTFUL_PAINT_MS.percentile
        const fieldFID = fieldMetrics.FIRST_INPUT_DELAY_MS.percentile
        const fieldLCP = fieldMetrics.LARGEST_CONTENTFUL_PAINT_MS.percentile
        const fieldCLS = fieldMetrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile

        // Construct FieldResult object
        const fieldResObj = {
          'test url': result.loadingExperience.id,
          fcp: fieldFCP,
          fid: fieldFID,
          lcp: fieldLCP,
          cls: fieldCLS / 100,
          date: moment().format('YYYY-MM-DD'),
        }
        // Push to fieldRes array
        fieldDataRes.push(fieldResObj)
      } else {
        console.log('No field data for this URL, extracting origin data instead...')

        // Otherwise Extract Origin Field metrics (if there are)
        const fieldFCP = fieldMetrics.FIRST_CONTENTFUL_PAINT_MS.percentile
        const fieldFID = fieldMetrics.FIRST_INPUT_DELAY_MS.percentile
        const fieldLCP = fieldMetrics.LARGEST_CONTENTFUL_PAINT_MS.percentile
        const fieldCLS = fieldMetrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile

        // Construct fieldResult object
        const fieldResObj = {
          'test url': result.loadingExperience.id,
          fcp: fieldFCP,
          fid: fieldFID,
          lcp: fieldLCP,
          cls: fieldCLS / 100,
          date: moment().format('YYYY-MM-DD'),
        }
        // Push to fieldOrigin array
        fieldOriginRes.push(fieldResObj)
      }
    }
  }
  // Write field results to CSV if there are results
  if (fieldOriginRes.length > 0) {
    fs.writeFileSync(`./results/client-origin-field.json`, JSON.stringify(fieldOriginRes, null, 2))
    fs.writeFileSync(`./results/client-origin-field.csv`, parse(fieldOriginRes))
  }
  if (fieldDataRes.length > 0) {
    fs.writeFileSync(`./results/client-field.json`, JSON.stringify(fieldDataRes, null, 2))
    fs.writeFileSync(`./results/client-field.csv`, parse(fieldDataRes))
  }
}

// Function to extract lab data from API
const getLabData = async (testNum) => {
  // Get URLs to test
  const urlList = await getUrls()

  // Store all results from each test
  const labAll = []

  // Loop through file
  for (const url of urlList) {
    for (let i = 0; i < testNum; i++) {
      console.log(`Requesting Lab data for ${url} Test #${i + 1}`)

      // Make request to extract lab data
      const result = await apiRequest(url).catch((err) =>
        console.log(`Error in the API request: ${err}`)
      )
      fs.writeFileSync('./api-response-example.json', JSON.stringify(result, null, 2))
      // Variable to make extraction cleaner
      const audit = result.lighthouseResult.audits

      // Extract Lab metrics
      const testUrl = result.lighthouseResult.finalUrl
      // const benchmarkIndex = result.lighthouseResult.environment.benchmarkIndex
      // const CPU = benchmarkCheck(benchmarkIndex)
      const TTFB = audit['server-response-time'].numericValue
      const TTI = audit.metrics.details.items[0].interactive
      const labFCP = audit.metrics.details.items[0].firstContentfulPaint
      const labLCP = audit.metrics.details.items[0].largestContentfulPaint
      const labCLS = parseFloat(audit['cumulative-layout-shift'].displayValue)
      const TBT = audit.metrics.details.items[0].totalBlockingTime
      const labMaxFID = audit.metrics.details.items[0].maxPotentialFID
      const speedIndex = audit.metrics.details.items[0].speedIndex
      const pageSize = parseFloat((audit['total-byte-weight'].numericValue / 1000000).toFixed(3))
      const date = moment().format('YYYY-MM-DD')

      // Construct object
      const finalObj = {
        testUrl,
        TTFB,
        labFCP,
        labLCP,
        labCLS,
        TTI,
        speedIndex,
        TBT,
        labMaxFID,
        pageSize,
        date,
      }
      labAll.push(finalObj)
    }
  }
  // Write results to CSV
  fs.writeFileSync(`./results/client-lab.json`, JSON.stringify(labAll, null, 2))
  fs.writeFileSync(`./results/client-lab.csv`, parse(labAll))
  console.timeEnd()
}

// Call getFieldData function
getFieldData()
// Call getLabData function (add number of test to run per URL)
getLabData(1)
