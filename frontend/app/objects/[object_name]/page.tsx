"use client";

import { useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import DynamicTable from "@/components/DynamicTable";
import DynamicRecordDrawer from "@/components/DynamicRecordDrawer";
import {
  useObjectByName,
  useDynamicRecords,
  useCreateRecord,
  useUpdateRecord,
  useDeleteRecord,
  useEnrichRecord,
} from "@/hooks/useDynamicObject";
import { DynamicRecord } from "@/lib/api";
import { Loader2, AlertTriangle } from "lucide-react";

const PAGE_SIZE = 50;

export default function DynamicObjectPage() {
  const params = useParams();
  const objectName = String(params.object_name || "");

  const [search, setSearch] = useState("");
  const [offset, setOffset] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<DynamicRecord | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<DynamicRecord | null>(null);

  const {
    data: objData,
    isLoading: objLoading,
    error: objError,
  } = useObjectByName(objectName);

  const {
    data: recordsData,
    isLoading: recordsLoading,
  } = useDynamicRecords(objectName, {
    search: search || undefined,
    limit: PAGE_SIZE,
    offset,
  });

  const createMutation = useCreateRecord(objectName);
  const updateMutation = useUpdateRecord(objectName);
  const deleteMutation = useDeleteRecord(objectName);
  const enrichMutation = useEnrichRecord(objectName);
  const [enrichingId, setEnrichingId] = useState<string | null>(null);

  const handleCreate = useCallback(() => {
    setEditingRecord(null);
    setDrawerOpen(true);
  }, []);

  const handleEdit = useCallback((record: DynamicRecord) => {
    setEditingRecord(record);
    setDrawerOpen(true);
  }, []);

  const handleDelete = useCallback((record: DynamicRecord) => {
    setDeleteConfirm(record);
  }, []);

  const handleSave = useCallback(
    (payload: { label: string; data: Record<string, any> }) => {
      if (editingRecord) {
        updateMutation.mutate(
          { recordId: editingRecord.id, payload },
          {
            onSuccess: () => {
              setDrawerOpen(false);
              setEditingRecord(null);
            },
          }
        );
      } else {
        createMutation.mutate(payload, {
          onSuccess: () => {
            setDrawerOpen(false);
            setOffset(0);
          },
        });
      }
    },
    [editingRecord, createMutation, updateMutation]
  );

  const handleConfirmDelete = useCallback(() => {
    if (!deleteConfirm) return;
    deleteMutation.mutate(deleteConfirm.id, {
      onSuccess: () => {
        setDeleteConfirm(null);
      },
    });
  }, [deleteConfirm, deleteMutation]);

  const handleEnrich = useCallback((record: DynamicRecord) => {
    setEnrichingId(record.id);
    enrichMutation.mutate(record.id, {
      onSuccess: () => {
        setEnrichingId(null);
      },
      onError: () => {
        setEnrichingId(null);
      },
    });
  }, [enrichMutation]);

  const isSaving = createMutation.isPending || updateMutation.isPending;

  if (objLoading) {
    return (
      <div className="min-h-screen bg-eko-graphite">
        <Navbar />
        <div className="flex items-center justify-center pt-32">
          <Loader2 className="w-8 h-8 animate-spin text-eko-blue" />
        </div>
      </div>
    );
  }

  if (objError || !objData) {
    return (
      <div className="min-h-screen bg-eko-graphite">
        <Navbar />
        <div className="flex flex-col items-center justify-center pt-32 text-gray-500 gap-3">
          <AlertTriangle className="w-8 h-8 text-red-400" />
          <p className="text-lg font-medium">
            {objError ? `Error cargando objeto: ${(objError as Error).message}` : `Objeto "${objectName}" no encontrado`}
          </p>
          <p className="text-sm text-gray-500">
            Asegúrate de que el objeto esté registrado en el motor de metadatos.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <DynamicTable
          object={objData}
          records={recordsData?.items || []}
          total={recordsData?.total || 0}
          loading={recordsLoading}
          onCreate={handleCreate}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onEnrich={handleEnrich}
          enrichingId={enrichingId}
          search={search}
          onSearchChange={setSearch}
          limit={PAGE_SIZE}
          offset={offset}
          onOffsetChange={setOffset}
        />
      </main>

      {/* Create/Edit Drawer */}
      <DynamicRecordDrawer
        object={objData}
        record={editingRecord}
        open={drawerOpen}
        onClose={() => {
          setDrawerOpen(false);
          setEditingRecord(null);
        }}
        onSave={handleSave}
        saving={isSaving}
      />

      {/* Delete confirmation modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-sm rounded-xl border border-white/10 bg-eko-graphite shadow-2xl p-6">
            <h3 className="text-lg font-bold font-display mb-2">Confirmar eliminación</h3>
            <p className="text-sm text-gray-400 mb-6">
              ¿Eliminar <strong className="text-white">{deleteConfirm.label}</strong>? Esta acción no se puede deshacer.
            </p>
            <div className="flex items-center justify-end gap-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-gray-300 hover:bg-white/10 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleConfirmDelete}
                disabled={deleteMutation.isPending}
                className="flex items-center gap-2 rounded-lg bg-red-500 px-4 py-2 text-sm font-medium hover:bg-red-600 disabled:opacity-50 transition-colors"
              >
                {deleteMutation.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  "Eliminar"
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
