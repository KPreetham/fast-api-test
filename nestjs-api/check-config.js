const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

console.log('Environment Variables:');
console.log('PORT:', process.env.PORT);
console.log('HOST:', process.env.HOST);
console.log('DATABASE_URL:', process.env.DATABASE_URL);
console.log('DATABASE_SSL:', process.env.DATABASE_SSL);
console.log('JWT_SECRET_KEY:', process.env.JWT_SECRET_KEY ? 'SET' : 'NOT SET');
console.log('JWT_ALGORITHM:', process.env.JWT_ALGORITHM);
console.log(
  'JWT_ACCESS_TOKEN_EXPIRE_MINUTES:',
  process.env.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
);
console.log('DEBUG:', process.env.DEBUG);

console.log('\nConfiguration:');
const config = {
  database: {
    url:
      process.env.DATABASE_URL ||
      'postgresql://username:password@localhost:5432/database',
    ssl: process.env.DATABASE_SSL === 'true',
  },
  jwt: {
    secret: process.env.JWT_SECRET_KEY || 'your-secret-key',
    algorithm: process.env.JWT_ALGORITHM || 'HS256',
    expiresIn: parseInt(process.env.JWT_ACCESS_TOKEN_EXPIRE_MINUTES) || 30,
  },
  server: {
    host: process.env.HOST || 'localhost',
    port: parseInt(process.env.PORT) || 3000,
    debug: process.env.DEBUG === 'true',
  },
};

console.log(JSON.stringify(config, null, 2));
