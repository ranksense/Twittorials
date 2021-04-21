/* Modules */
import axios from 'axios'

/* API Parameters */
const endpoint = 'https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed' // Endpoint
const key = '' // API Key
const device = 'mobile' // Test viewport. 'desktop' also available

// Custom function to request PageSpeed API
export const apiRequest = async (url) => {
  const { data } = await axios(`${endpoint}?url=${url}&strategy=${device}&key=${key}`)
  return data
}
