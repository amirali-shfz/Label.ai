import api from '../apiService';
import { User } from './userModel';

const userApi = {
  getUser: async (): Promise<User> => {
    const user : any = await api.get('/user');
    return new User({userId: user.uid, username: user.username, trust:user.trust})
  },

  createUser: async (firstName: string, lastName: string, username: string, password:string) => {
    await api.post('/user', {
      firstName,
      lastName,
      username,
      password
    });
  },

};

export default userApi;