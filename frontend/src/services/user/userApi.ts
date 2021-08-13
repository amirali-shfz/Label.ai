import api from "../apiService";
import { User } from "./userModel";

const userApi = {
  getUsersMap: async (): Promise<User> => {
    const res: any = await api.get("/members/all");
    const users = res.data.reduce((map: any, user: any) => {
      map[user.username] = { trust: user.trust, userId: user.userId };
      return map;
    }, {});
    return users;
  },

  createUser: async (
    firstName: string,
    lastName: string,
    username: string,
    password: string
  ) => {
    await api.post("/members", {
      firstName,
      lastName,
      username,
      password,
    });
  },
};

export default userApi;
