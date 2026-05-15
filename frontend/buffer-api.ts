const BUFFER_API_URL = "https://api.buffer.com";
const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

export async function bufferGraphQL(query: string, variables?: Record<string, any>) {
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
  return data.data;
}

export async function getOrganizationId(): Promise<string> {
  const data = await bufferGraphQL(`
    query {
      account {
        organizations {
          id
        }
      }
    }
  `);
  return data.account.organizations[0]?.id || "";
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
