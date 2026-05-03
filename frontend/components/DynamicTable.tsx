"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  Search,
  Plus,
  Loader2,
  MoreHorizontal,
  Pencil,
  Trash2,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  X,
  Sparkles,
} from "lucide-react";
import { ObjectMetadata, FieldMetadata, DynamicRecord, View } from "@/lib/api";

interface DynamicTableProps {
  object: ObjectMetadata;
  view?: View;
  records: DynamicRecord[];
  total: number;
  loading: boolean;
  onCreate: () => void;
  onEdit: (record: DynamicRecord) => void;
  onDelete: (record: DynamicRecord) => void;
  onEnrich?: (record: DynamicRecord) => void;
  enrichingId?: string | null;
  search?: string;
  onSearchChange?: (q: string) => void;
  limit?: number;
  offset?: number;
  onOffsetChange?: (offset: number) => void;
}

function fieldTypeIcon(type: string) {
  switch (type) {
    case "EMAIL":
      return "@";
    case "PHONE":
      return "📞";
    case "URL":
      return "🔗";
    case "CURRENCY":
      return "$";
    case "DATE":
    case "DATE_TIME":
      return "📅";
    case "BOOLEAN":
      return "✓";
    case "NUMBER":
      return "#";
    default:
      return "";
  }
}

function formatCellValue(field: FieldMetadata, value: any): React.ReactNode {
  if (value == null || value === "") return <span className="text-gray-600">—</span>;

  switch (field.type) {
    case "BOOLEAN":
      return value ? (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-eko-green/20 text-eko-green text-xs font-medium">
          Sí
        </span>
      ) : (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-white/5 text-gray-400 text-xs font-medium">
          No
        </span>
      );
    case "CURRENCY":
      return (
        <span className="font-mono text-sm">
          {typeof value === "number" ? `$${value.toLocaleString()}` : String(value)}
        </span>
      );
    case "NUMBER":
      return <span className="font-mono text-sm">{typeof value === "number" ? value.toLocaleString() : String(value)}</span>;
    case "EMAIL":
      return (
        <a href={`mailto:${value}`} className="text-eko-blue hover:underline text-sm" onClick={(e) => e.stopPropagation()}>
          {String(value)}
        </a>
      );
    case "PHONE":
      return (
        <a href={`tel:${value}`} className="text-eko-blue hover:underline text-sm" onClick={(e) => e.stopPropagation()}>
          {String(value)}
        </a>
      );
    case "URL": {
      const url = String(value);
      return (
        <a href={url.startsWith("http") ? url : `https://${url}`} target="_blank" rel="noopener noreferrer" className="text-eko-blue hover:underline text-sm" onClick={(e) => e.stopPropagation()}>
          {url.length > 30 ? url.slice(0, 30) + "…" : url}
        </a>
      );
    }
    case "SELECT":
      if (field.options) {
        const opt = field.options.find((o) => o.value === value);
        const color = opt?.color || "#334155";
        return (
          <span
            className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
            style={{ backgroundColor: `${color}20`, color }}
          >
            {opt?.label || String(value)}
          </span>
        );
      }
      return <span className="text-sm">{String(value)}</span>;
    case "MULTI_SELECT":
      if (Array.isArray(value) && field.options) {
        return (
          <div className="flex flex-wrap gap-1">
            {value.map((v, i) => {
              const opt = field.options?.find((o) => o.value === v);
              const color = opt?.color || "#334155";
              return (
                <span
                  key={i}
                  className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                  style={{ backgroundColor: `${color}20`, color }}
                >
                  {opt?.label || String(v)}
                </span>
              );
            })}
          </div>
        );
      }
      return <span className="text-sm">{String(value)}</span>;
    case "DATE":
    case "DATE_TIME":
      try {
        const d = new Date(value);
        return (
          <span className="text-sm text-gray-400">
            {field.type === "DATE_TIME"
              ? d.toLocaleString("es-ES", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })
              : d.toLocaleDateString("es-ES", { day: "2-digit", month: "short", year: "numeric" })}
          </span>
        );
      } catch {
        return <span className="text-sm">{String(value)}</span>;
      }
    default:
      return <span className="text-sm">{String(value)}</span>;
  }
}

export default function DynamicTable({
  object,
  view,
  records,
  total,
  loading,
  onCreate,
  onEdit,
  onDelete,
  onEnrich,
  enrichingId,
  search,
  onSearchChange,
  limit = 50,
  offset = 0,
  onOffsetChange,
}: DynamicTableProps) {
  const [menuOpenId, setMenuOpenId] = useState<string | null>(null);
  const [sortField, setSortField] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  // Determine which fields to show
  const visibleFields = useMemo(() => {
    if (view?.view_fields?.length) {
      const visible = view.view_fields
        .filter((vf) => vf.is_visible)
        .sort((a, b) => a.position - b.position)
        .map((vf) => object.fields.find((f) => f.id === vf.field_metadata_id))
        .filter(Boolean) as FieldMetadata[];
      if (visible.length) return visible;
    }
    // Default: show label field + first 6 non-system fields
    const labelField = object.fields.find((f) => f.is_label_field);
    const others = object.fields
      .filter((f) => !f.is_system && f.id !== labelField?.id)
      .slice(0, 6);
    return labelField ? [labelField, ...others] : others;
  }, [object.fields, view]);

  // Client-side sort
  const sortedRecords = useMemo(() => {
    if (!sortField) return records;
    const field = object.fields.find((f) => f.name === sortField);
    if (!field) return records;
    const dir = sortDir === "asc" ? 1 : -1;
    return [...records].sort((a, b) => {
      const av = a.data[sortField];
      const bv = b.data[sortField];
      if (av == null && bv == null) return 0;
      if (av == null) return 1 * dir;
      if (bv == null) return -1 * dir;
      if (typeof av === "number" && typeof bv === "number") return (av - bv) * dir;
      return String(av).localeCompare(String(bv)) * dir;
    });
  }, [records, sortField, sortDir, object.fields]);

  const handleSort = (fieldName: string) => {
    if (sortField === fieldName) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortField(fieldName);
      setSortDir("asc");
    }
  };

  const totalPages = Math.ceil(total / limit) || 1;
  const currentPage = Math.floor(offset / limit) + 1;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold font-display">{object.label_plural}</h1>
          <p className="text-gray-400 text-sm">
            {total} {total === 1 ? object.label_singular.toLowerCase() : object.label_plural.toLowerCase()}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {onSearchChange && (
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="text"
                value={search || ""}
                onChange={(e) => onSearchChange(e.target.value)}
                placeholder={`Buscar ${object.label_plural.toLowerCase()}...`}
                className="w-64 rounded-lg border border-white/10 bg-white/5 pl-10 pr-4 py-2 text-sm focus:border-eko-blue focus:outline-none"
              />
              {search && (
                <button
                  onClick={() => onSearchChange("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          )}
          <button
            onClick={onCreate}
            className="flex items-center gap-2 rounded-lg bg-eko-blue px-4 py-2 text-sm font-medium hover:bg-eko-blue-dark transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span className="hidden sm:inline">Nuevo {object.label_singular}</span>
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            <thead>
              <tr className="border-b border-white/5 text-left text-xs text-gray-500 uppercase">
                {visibleFields.map((field) => (
                  <th
                    key={field.id}
                    className="px-4 py-3 font-medium cursor-pointer select-none hover:text-gray-300 transition-colors"
                    onClick={() => handleSort(field.name)}
                  >
                    <div className="flex items-center gap-1">
                      {field.label}
                      {sortField === field.name ? (
                        sortDir === "asc" ? (
                          <ArrowUp className="w-3 h-3" />
                        ) : (
                          <ArrowDown className="w-3 h-3" />
                        )
                      ) : (
                        <ArrowUpDown className="w-3 h-3 opacity-0 group-hover:opacity-100" />
                      )}
                    </div>
                  </th>
                ))}
                <th className="px-4 py-3 w-10" />
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {loading ? (
                <tr>
                  <td colSpan={visibleFields.length + 1} className="px-4 py-12 text-center">
                    <Loader2 className="w-6 h-6 animate-spin text-eko-blue mx-auto" />
                  </td>
                </tr>
              ) : sortedRecords.length === 0 ? (
                <tr>
                  <td colSpan={visibleFields.length + 1} className="px-4 py-12 text-center text-gray-500 text-sm">
                    No se encontraron {object.label_plural.toLowerCase()}.
                  </td>
                </tr>
              ) : (
                sortedRecords.map((record) => (
                  <tr
                    key={record.id}
                    className="hover:bg-white/[0.02] transition-colors group"
                  >
                    {visibleFields.map((field) => (
                      <td key={field.id} className="px-4 py-3">
                        {field.is_label_field ? (
                          <button
                            onClick={() => onEdit(record)}
                            className="text-sm font-medium hover:text-eko-blue transition-colors text-left"
                          >
                            {record.label}
                          </button>
                        ) : (
                          formatCellValue(field, record.data[field.name])
                        )}
                      </td>
                    ))}
                    <td className="px-4 py-3 relative">
                      <button
                        onClick={() => setMenuOpenId(menuOpenId === record.id ? null : record.id)}
                        className="p-1 rounded-lg hover:bg-white/10 text-gray-500 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <MoreHorizontal className="w-4 h-4" />
                      </button>
                      {menuOpenId === record.id && (
                        <div className="absolute right-2 top-full mt-1 w-40 rounded-lg border border-white/10 bg-eko-graphite shadow-xl z-50 overflow-hidden">
                          <button
                            onClick={() => {
                              onEdit(record);
                              setMenuOpenId(null);
                            }}
                            className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 transition-colors"
                          >
                            <Pencil className="w-3.5 h-3.5" />
                            Editar
                          </button>
                          {onEnrich && (
                            <button
                              onClick={() => {
                                onEnrich(record);
                                setMenuOpenId(null);
                              }}
                              disabled={enrichingId === record.id}
                              className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-eko-blue hover:bg-eko-blue/10 transition-colors disabled:opacity-50"
                            >
                              {enrichingId === record.id ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              ) : (
                                <Sparkles className="w-3.5 h-3.5" />
                              )}
                              Enriquecer
                            </button>
                          )}
                          <button
                            onClick={() => {
                              onDelete(record);
                              setMenuOpenId(null);
                            }}
                            className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 transition-colors"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            Eliminar
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {onOffsetChange && total > limit && (
        <div className="flex items-center justify-between px-2">
          <div className="text-xs text-gray-500">
            Página {currentPage} de {totalPages}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onOffsetChange(Math.max(0, offset - limit))}
              disabled={offset <= 0}
              className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-medium text-gray-300 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              ← Anterior
            </button>
            <button
              onClick={() => onOffsetChange(offset + limit)}
              disabled={offset + limit >= total}
              className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-medium text-gray-300 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              Siguiente →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
