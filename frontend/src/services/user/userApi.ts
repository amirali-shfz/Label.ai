import api from '../apiService';
import { User } from './userModel';

const userApi = {
  getUser: async (): Promise<User> => {
    const res : any = await api.get('/members/all');
    const user = res.data[0]
    return new User({userId: user.uid, username: user.username, trust:user.trust})
  },

  createUser: async (firstName: string, lastName: string, username: string, password:string) => {
    await api.post('/members', {
      firstName,
      lastName,
      username,
      password
    });
  },

};

export default userApi;