import { getCached, setCache } from "./api-cache";

const BUFFER_API_URL = "https://api.buffer.com";
const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

// Cache GraphQL responses for 30s to avoid Buffer rate limits
export async function bufferGraphQL(query: string, variables?: Record<string, any>) {
  const cacheKey = "buffer:gql:" + Buffer.from(query).toString("base64").slice(0, 64);
  const cached = getCached<any>(cacheKey);
  if (cached) return cached;

  const res = await fetch(BUFFER_API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${BUFFER_API_KEY}`,
    },
    body: JSON.stringify({ query, variables }),
  });

  const data = await res.json();
  if (data.errors) {
    throw new Error(data.errors[0].message);
  }
  setCache(cacheKey, data.data, 30000);
  return data.data;
}

// Cache org ID for 5 minutes (rarely changes)
export async function getOrganizationId(): Promise<string> {
  const cached = getCached<string>("buffer:orgId");
  if (cached) return cached;

  const data = await bufferGraphQL(`
    query {
      account {
        organizations {
          id
        }
      }
    }
  `);
  const orgId = data.account.organizations[0]?.id || "";
  if (orgId) setCache("buffer:orgId", orgId, 300000);
  return orgId;
}

export async function getChannels() {
  const orgId = await getOrganizationId();
  const data = await bufferGraphQL(`
    query {
      channels(input: { organizationId: "${orgId}" }) {
        id
        name
        service
        isDisconnected
      }
    }
  `);
  return data.channels || [];
}
