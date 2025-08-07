import { ConfigService } from '@nestjs/config';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const configService = app.get(ConfigService);

  const port = configService.get<number>('server.port') || 3000;
  const host = configService.get<string>('server.host') || 'localhost';

  // Validate port to prevent binding to privileged ports
  if (port < 1024) {
    console.warn(
      `Warning: Port ${port} requires root privileges. Consider using a port >= 1024 for development.`,
    );
  }

  await app.listen(port, host);
  console.log(`Application is running on: http://${host}:${port}`);
}
bootstrap();
