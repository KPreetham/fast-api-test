import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Post } from '../entities/post.entity';
import { User } from '../entities/user.entity';

@Injectable()
export class PostsService {
  constructor(
    @InjectRepository(Post)
    private postRepository: Repository<Post>,
  ) {}

  async findPostsByUserId(userId: number): Promise<Post[]> {
    return this.postRepository.find({
      where: { user_id: userId },
      order: { created_at: 'DESC' },
    });
  }

  async findPostsByUser(user: User): Promise<Post[]> {
    return this.findPostsByUserId(user.id);
  }
}
