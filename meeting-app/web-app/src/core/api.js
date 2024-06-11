import axios from 'axios'
import { Platform } from 'react-native'


export const ADDRESS = Platform.OS === 'ios'
 	? 'localhost:8000'
	: '127.0.0.1:8000'

const api = axios.create({
	baseURL: 'http://' + ADDRESS,
	headers: {
		'Content-Type': 'application/json'
	}
})

export default api