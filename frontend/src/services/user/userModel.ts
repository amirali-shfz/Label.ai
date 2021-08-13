export class User {
  readonly userId: string;
  readonly username: string;
  readonly trust: string;

  constructor(body: any = {}) {
    this.userId = body.userId;
    this.username = body.username;
    this.trust = body.trust;
  }
}
