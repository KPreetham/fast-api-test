import { IsNotEmpty, IsString } from 'class-validator';

export class PostCreateDto {
  @IsString()
  @IsNotEmpty()
  title: string;

  @IsString()
  @IsNotEmpty()
  content: string;
}

export class PostDto {
  id: number;
  user_id: number;
  title: string;
  content: string;
  created_at: Date;
  updated_at: Date;
}

export class UserWithPostsDto {
  id: number;
  email: string;
  name: string;
  created_at: Date;
  updated_at: Date;
  posts: PostDto[];
}
