import { slugify } from "./textConverter";

const taxonomyFilter = (posts: any[], name: string, key: any) =>
    posts.filter((post) =>
        post.data[name].map((item: string) => slugify(item)).includes(key)
    );

export default taxonomyFilter;
