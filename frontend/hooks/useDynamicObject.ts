"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { metadataApi, viewsApi, dynamicDataApi, ObjectMetadata, View, DynamicRecord } from "@/lib/api";

// ------------------------------------------------------------------
// Queries
// ------------------------------------------------------------------

export function useObjects() {
  return useQuery({
    queryKey: ["metadata", "objects"],
    queryFn: async () => {
      const res = await metadataApi.listObjects();
      return res.data;
    },
  });
}

export function useObjectByName(name: string) {
  return useQuery({
    queryKey: ["metadata", "object", name],
    queryFn: async () => {
      const res = await metadataApi.getObjectByName(name);
      return res.data;
    },
    enabled: !!name,
  });
}

export function useViews(objectMetadataId?: string) {
  return useQuery({
    queryKey: ["views", objectMetadataId],
    queryFn: async () => {
      const res = await viewsApi.list(objectMetadataId);
      return res.data;
    },
    enabled: !!objectMetadataId,
  });
}

export function useDynamicRecords(
  objectName: string,
  options?: {
    search?: string;
    limit?: number;
    offset?: number;
  }
) {
  return useQuery({
    queryKey: ["dynamic-data", objectName, options],
    queryFn: async () => {
      const res = await dynamicDataApi.list(objectName, options);
      return res.data;
    },
    enabled: !!objectName,
  });
}

// ------------------------------------------------------------------
// Mutations
// ------------------------------------------------------------------

export function useCreateRecord(objectName: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: { label: string; data: Record<string, any> }) => {
      const res = await dynamicDataApi.create(objectName, payload);
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["dynamic-data", objectName] });
    },
  });
}

export function useUpdateRecord(objectName: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({
      recordId,
      payload,
    }: {
      recordId: string;
      payload: { label?: string; data?: Record<string, any> };
    }) => {
      const res = await dynamicDataApi.update(objectName, recordId, payload);
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["dynamic-data", objectName] });
    },
  });
}

export function useDeleteRecord(objectName: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (recordId: string) => {
      await dynamicDataApi.delete(objectName, recordId);
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["dynamic-data", objectName] });
    },
  });
}

export function useEnrichRecord(objectName: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (recordId: string) => {
      const res = await dynamicDataApi.enrich(objectName, recordId);
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["dynamic-data", objectName] });
    },
  });
}
