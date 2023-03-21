//import { useState, useEffect } from 'react'
//import axios from 'axios';
//import { API_SERVER } from './constant.js';
//
//export default function useApi(api) {
//  const [ result, setResult ] = useState([])
//  useEffect(() => {
//    axios.get(API_SERVER + api)
//         .then(response => setResult(response.data));
//  }, [])
//  return result;
//}
