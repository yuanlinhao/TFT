import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001'; // Change this when deploying

export const fetchChampions = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/champions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching champions:', error);
    return [];
  }
};

export const fetchItems = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/items`);
    return response.data;
  } catch (error) {
    console.error('Error fetching items:', error);
    return [];
  }
};
