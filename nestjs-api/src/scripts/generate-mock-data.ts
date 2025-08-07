import { NestFactory } from '@nestjs/core';
import { AppModule } from '../app.module';
import { UserCreateDto } from '../dto/user.dto';
import { PostsService } from '../posts/posts.service';
import { UsersService } from '../users/users.service';

async function generateMockData() {
  const app = await NestFactory.createApplicationContext(AppModule);

  const usersService = app.get(UsersService);
  const postsService = app.get(PostsService);

  try {
    // Create some test users
    const userData: UserCreateDto[] = [
      {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123',
      },
      {
        name: 'Jane Smith',
        email: 'jane@example.com',
        password: 'password123',
      },
      {
        name: 'Bob Johnson',
        email: 'bob@example.com',
        password: 'password123',
      },
    ];

    console.log('Creating users...');
    const users = [];
    for (const userDto of userData) {
      try {
        const user = await usersService.createUser(userDto);
        users.push(user);
        console.log(`Created user: ${user.name} (${user.email})`);
      } catch (error) {
        console.log(`User ${userDto.email} already exists, skipping...`);
      }
    }

    console.log('Mock data generation completed!');
  } catch (error) {
    console.error('Error generating mock data:', error);
  } finally {
    await app.close();
  }
}

generateMockData();
