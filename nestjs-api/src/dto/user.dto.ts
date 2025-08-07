import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';

export class UserCreateDto {
  @IsEmail()
  email: string;

  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @MinLength(6)
  password: string;
}

export class UserDto {
  id: number;
  email: string;
  name: string;
  created_at: Date;
  updated_at: Date;
}

export class TokenDto {
  access_token: string;
  token_type: string;
}

export class TokenDataDto {
  email?: string;
}
