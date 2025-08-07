import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectRepository } from '@nestjs/typeorm';
import * as bcrypt from 'bcrypt';
import { Repository } from 'typeorm';
import { TokenDataDto } from '../dto/user.dto';
import { User } from '../entities/user.entity';

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private jwtService: JwtService,
  ) {}

  async verifyPassword(
    plainPassword: string,
    hashedPassword: string,
  ): Promise<boolean> {
    return bcrypt.compare(plainPassword, hashedPassword);
  }

  async hashPassword(password: string): Promise<string> {
    const saltRounds = 10;
    return bcrypt.hash(password, saltRounds);
  }

  async createAccessToken(data: { sub: string }): Promise<string> {
    const payload = { sub: data.sub };
    return this.jwtService.signAsync(payload);
  }

  async verifyToken(token: string): Promise<TokenDataDto> {
    try {
      const payload = await this.jwtService.verifyAsync(token);
      return { email: payload.sub };
    } catch {
      throw new UnauthorizedException('Could not validate credentials');
    }
  }

  async validateUser(email: string, password: string): Promise<User> {
    const user = await this.userRepository.findOne({ where: { email } });
    if (user && (await this.verifyPassword(password, user.password))) {
      return user;
    }
    return null;
  }

  async findUserByEmail(email: string): Promise<User> {
    return this.userRepository.findOne({ where: { email } });
  }
}
