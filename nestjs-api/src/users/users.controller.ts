import {
  Body,
  Controller,
  Get,
  HttpException,
  HttpStatus,
  Post,
  Request,
  UseGuards,
} from '@nestjs/common';
import { AuthService } from '../auth/auth.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { PostDto } from '../dto/post.dto';
import { TokenDto, UserCreateDto, UserDto } from '../dto/user.dto';
import { User } from '../entities/user.entity';
import { PostsService } from '../posts/posts.service';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(
    private usersService: UsersService,
    private authService: AuthService,
    private postsService: PostsService,
  ) {}

  @Post('signup')
  async signup(@Body() userCreateDto: UserCreateDto): Promise<UserDto> {
    const user = await this.usersService.createUser(userCreateDto);
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      created_at: user.created_at,
      updated_at: user.updated_at,
    };
  }

  @Post('token')
  async login(
    @Body() loginDto: { username: string; password: string },
  ): Promise<TokenDto> {
    const user = await this.authService.validateUser(
      loginDto.username,
      loginDto.password,
    );
    if (!user) {
      throw new HttpException(
        'Incorrect email or password',
        HttpStatus.UNAUTHORIZED,
      );
    }

    const accessToken = await this.authService.createAccessToken({
      sub: user.email,
    });
    return {
      access_token: accessToken,
      token_type: 'bearer',
    };
  }

  @UseGuards(JwtAuthGuard)
  @Get('me')
  async getCurrentUser(@Request() req): Promise<UserDto> {
    const user = req.user as User;
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      created_at: user.created_at,
      updated_at: user.updated_at,
    };
  }

  @UseGuards(JwtAuthGuard)
  @Get('me/posts')
  async getUserPosts(@Request() req): Promise<PostDto[]> {
    const user = req.user as User;
    const posts = await this.postsService.findPostsByUser(user);
    return posts.map((post) => ({
      id: post.id,
      user_id: post.user_id,
      title: post.title,
      content: post.content,
      created_at: post.created_at,
      updated_at: post.updated_at,
    }));
  }
}
