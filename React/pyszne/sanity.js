import SanityClient from "@sanity/client";
import imageUriBuilder from "@sanity/image-url";

const client = SanityClient({
    projectId: "e75mzmdv",
    dataset: "production",
    useCdn: true,
    apiVersion: "2021-10-21"
});

const builder = imageUriBuilder(client);
export const urlFor = (source) => builder.image(source);

export default client;