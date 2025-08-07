export default () => ({
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
});
