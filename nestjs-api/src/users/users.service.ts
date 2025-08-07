import {
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { AuthService } from '../auth/auth.service';
import { UserCreateDto } from '../dto/user.dto';
import { User } from '../entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private authService: AuthService,
  ) {}

  async createUser(userCreateDto: UserCreateDto): Promise<User> {
    // Check if user already exists
    const existingUser = await this.userRepository.findOne({
      where: { email: userCreateDto.email },
    });

    if (existingUser) {
      throw new ConflictException('Email already registered');
    }

    // Hash password and create user
    const hashedPassword = await this.authService.hashPassword(
      userCreateDto.password,
    );
    const user = this.userRepository.create({
      email: userCreateDto.email,
      name: userCreateDto.name,
      password: hashedPassword,
    });

    return this.userRepository.save(user);
  }

  async findAllUsers(): Promise<User[]> {
    return this.userRepository.find();
  }

  async findUserById(id: number): Promise<User> {
    const user = await this.userRepository.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException('User not found');
    }
    return user;
  }

  async findUserByEmail(email: string): Promise<User> {
    return this.userRepository.findOne({ where: { email } });
  }

  async getRandomUser(): Promise<User> {
    const users = await this.userRepository.find();
    if (users.length === 0) {
      throw new NotFoundException('No users found in database');
    }

    const randomIndex = Math.floor(Math.random() * users.length);
    return users[randomIndex];
  }
}
