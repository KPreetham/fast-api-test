const axios = require('axios');

const BASE_URL = 'http://localhost:3000';

async function testAPI() {
  try {
    console.log('Testing NestJS API...\n');

    // Test root endpoint
    console.log('1. Testing root endpoint...');
    const rootResponse = await axios.get(`${BASE_URL}/`);
    console.log('Response:', rootResponse.data);

    // Test signup
    console.log('\n2. Testing user signup...');
    const signupResponse = await axios.post(`${BASE_URL}/users/signup`, {
      name: 'Test User',
      email: 'test@example.com',
      password: 'password123',
    });
    console.log('Signup response:', signupResponse.data);

    // Test login
    console.log('\n3. Testing user login...');
    const loginResponse = await axios.post(`${BASE_URL}/users/token`, {
      username: 'test@example.com',
      password: 'password123',
    });
    console.log('Login response:', loginResponse.data);

    const token = loginResponse.data.access_token;

    // Test protected endpoint
    console.log('\n4. Testing protected endpoint...');
    const meResponse = await axios.get(`${BASE_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log('Protected endpoint response:', meResponse.data);

    // Test random endpoint
    console.log('\n5. Testing random endpoint...');
    const randomResponse = await axios.get(`${BASE_URL}/random`);
    console.log('Random endpoint response:', randomResponse.data);

    console.log('\n✅ All tests passed!');
  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

testAPI();
