import axios from 'axios';

export async function sendMaintenanceMessage(sender, content) {
  return await axios.post('http://localhost:5000/api/maintenance/messages/', {
    sender,
    content,
    date: new Date().toISOString()
  });
}
