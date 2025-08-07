import {
  Controller,
  Get,
  HttpException,
  HttpStatus,
  Res,
} from '@nestjs/common';
import { Response } from 'express';
import { AppService } from './app.service';
import { AuthService } from './auth/auth.service';
import { PostsService } from './posts/posts.service';
import { UsersService } from './users/users.service';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private usersService: UsersService,
    private postsService: PostsService,
    private authService: AuthService,
  ) {}

  @Get()
  getHello(): { message: string; docs: string } {
    return { message: 'Welcome to NestJS Demo', docs: '/docs' };
  }

  @Get('random')
  async getRandomEndpoint() {
    // Generate random integer from 1-1000
    const randomNumber = Math.floor(Math.random() * 1000) + 1;

    // Get a random user from the database
    const randomUser = await this.usersService.getRandomUser();

    // Create JWT token for the random user
    const accessToken = await this.authService.createAccessToken({
      sub: randomUser.email,
    });

    // Decode the JWT token to verify it
    try {
      const tokenData = await this.authService.verifyToken(accessToken);
      if (tokenData.email !== randomUser.email) {
        throw new HttpException(
          'JWT token verification failed',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    } catch (error) {
      throw new HttpException(
        `JWT token decoding failed: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }

    // Get all posts for the user
    const userPosts = await this.postsService.findPostsByUser(randomUser);

    return {
      random_number: randomNumber,
      user: {
        id: randomUser.id,
        name: randomUser.name,
        email: randomUser.email,
      },
      jwt_token: accessToken,
      posts: userPosts.map((post) => ({
        id: post.id,
        title: post.title,
        content: post.content,
        created_at: post.created_at,
        updated_at: post.updated_at,
      })),
    };
  }

  @Get('loaderio-1169617544508734aa5dc4919f421add')
  getLoaderIo(@Res() res: Response) {
    res.type('text/plain');
    res.send('loaderio-1169617544508734aa5dc4919f421add');
  }
}
