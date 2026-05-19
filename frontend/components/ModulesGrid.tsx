"use client";

import { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  rectSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { ArrowRight, X, Plus, Pencil, Check, GripVertical, LucideIcon } from "lucide-react";

export interface ModuleDef {
  href: string;
  label: string;
  subtitle: string;
  icon: LucideIcon;
  color: string;
  badgeKey?: "unread";
}

interface ModulesGridProps {
  modules: ModuleDef[];
  unreadCount?: number;
}

// v2 bump (2026-05-19): added /landing-pages and /billing modules + reorganized
// the canonical order to follow the sales funnel (acquire → engage → close →
// grow → ops). Bumping the key forces every browser to pick up the new default
// instead of preserving the v1 order (which was incomplete).
const LS_ORDER = "eko_dashboard_modules_order_v2";
const LS_HIDDEN = "eko_dashboard_modules_hidden_v2";

function loadOrder(canonical: string[]): string[] {
  if (typeof window === "undefined") return canonical;
  try {
    const raw = window.localStorage.getItem(LS_ORDER);
    if (!raw) return canonical;
    const saved: string[] = JSON.parse(raw);
    const valid = saved.filter((h) => canonical.includes(h));
    // append any newly-introduced modules that aren't yet in saved order
    for (const h of canonical) if (!valid.includes(h)) valid.push(h);
    return valid;
  } catch {
    return canonical;
  }
}

function loadHidden(): Set<string> {
  if (typeof window === "undefined") return new Set();
  try {
    const raw = window.localStorage.getItem(LS_HIDDEN);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch {
    return new Set();
  }
}

interface SortableModuleProps {
  mod: ModuleDef;
  badge?: number;
  editMode: boolean;
  onRemove: (href: string) => void;
}

function SortableModule({ mod, badge, editMode, onRemove }: SortableModuleProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: mod.href,
    disabled: !editMode,
  });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
    zIndex: isDragging ? 10 : undefined,
  };

  const cardClass =
    "group relative flex flex-col items-center gap-2 rounded-xl border border-white/5 bg-white/[0.02] p-4 hover:bg-white/5 hover:border-white/10 transition-all";

  // In edit mode the card is NOT a link — it's a div the user can grab.
  if (editMode) {
    return (
      <div
        ref={setNodeRef}
        style={style}
        data-dnd-dragging={isDragging ? "true" : "false"}
        className={`${cardClass} cursor-grab active:cursor-grabbing select-none touch-none`}
        {...attributes}
        {...listeners}
      >
        <button
          type="button"
          onPointerDown={(e) => e.stopPropagation()}
          onClick={(e) => {
            e.stopPropagation();
            e.preventDefault();
            onRemove(mod.href);
          }}
          className="absolute -top-1.5 -left-1.5 z-20 flex items-center justify-center w-5 h-5 rounded-full bg-red-500 text-white shadow-lg hover:bg-red-600 transition-colors"
          aria-label={`Remove ${mod.label}`}
          title={`Quitar ${mod.label}`}
        >
          <X className="w-3 h-3" strokeWidth={3} />
        </button>
        <div className="absolute top-1.5 right-1.5 text-gray-600">
          <GripVertical className="w-3.5 h-3.5" />
        </div>
        <div className={`p-2.5 rounded-lg ${mod.color}`}>
          <mod.icon className="w-5 h-5" />
        </div>
        <div className="text-center">
          <p className="text-sm font-medium">{mod.label}</p>
          <p className="text-[10px] text-gray-500 mt-0.5">{mod.subtitle}</p>
        </div>
        {badge !== undefined && badge > 0 && (
          <span className="absolute top-2 right-7 flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-red-500 text-white text-[10px] font-bold">
            {badge > 99 ? "99+" : badge}
          </span>
        )}
      </div>
    );
  }

  // Normal mode: behaves exactly like before — a link.
  return (
    <Link href={mod.href} className={cardClass}>
      <div className={`p-2.5 rounded-lg ${mod.color}`}>
        <mod.icon className="w-5 h-5" />
      </div>
      <div className="text-center">
        <p className="text-sm font-medium group-hover:text-white transition-colors">
          {mod.label}
        </p>
        <p className="text-[10px] text-gray-500 mt-0.5">{mod.subtitle}</p>
      </div>
      {badge !== undefined && badge > 0 && (
        <span className="absolute top-2 right-2 flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-red-500 text-white text-[10px] font-bold">
          {badge > 99 ? "99+" : badge}
        </span>
      )}
      <ArrowRight className="w-3.5 h-3.5 text-gray-600 group-hover:text-gray-400 transition-colors mt-1" />
    </Link>
  );
}

export default function ModulesGrid({ modules, unreadCount }: ModulesGridProps) {
  const canonicalHrefs = useMemo(() => modules.map((m) => m.href), [modules]);
  const modulesByHref = useMemo(
    () => Object.fromEntries(modules.map((m) => [m.href, m])),
    [modules]
  );

  const [order, setOrder] = useState<string[]>(canonicalHrefs);
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const [editMode, setEditMode] = useState(false);
  const [showPicker, setShowPicker] = useState(false);

  // Hydrate from localStorage once on mount (avoids SSR mismatch)
  useEffect(() => {
    setOrder(loadOrder(canonicalHrefs));
    setHidden(loadHidden());
  }, [canonicalHrefs]);

  // Persist
  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(LS_ORDER, JSON.stringify(order));
  }, [order]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(LS_HIDDEN, JSON.stringify(Array.from(hidden)));
  }, [hidden]);

  // Esc exits edit mode
  useEffect(() => {
    if (!editMode) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setEditMode(false);
        setShowPicker(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [editMode]);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  const visibleHrefs = order.filter((h) => !hidden.has(h) && modulesByHref[h]);
  const hiddenList = canonicalHrefs.filter((h) => hidden.has(h));

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;
    setOrder((prev) => {
      const oldIdx = prev.indexOf(String(active.id));
      const newIdx = prev.indexOf(String(over.id));
      if (oldIdx < 0 || newIdx < 0) return prev;
      return arrayMove(prev, oldIdx, newIdx);
    });
  };

  const handleRemove = (href: string) => {
    setHidden((prev) => {
      const next = new Set(prev);
      next.add(href);
      return next;
    });
  };

  const handleAdd = (href: string) => {
    setHidden((prev) => {
      const next = new Set(prev);
      next.delete(href);
      return next;
    });
    // ensure it's at the end of order (in case it was reset)
    setOrder((prev) => (prev.includes(href) ? prev : [...prev, href]));
    if (hiddenList.length <= 1) setShowPicker(false);
  };

  const handleResetLayout = () => {
    setOrder(canonicalHrefs);
    setHidden(new Set());
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-medium text-gray-400 uppercase tracking-wider flex items-center gap-2">
          Módulos
          {editMode && (
            <span className="text-[10px] font-normal normal-case text-gray-500">
              · arrastra para reordenar · click ✕ para quitar
            </span>
          )}
        </h2>
        <div className="flex items-center gap-2">
          {editMode && (
            <button
              type="button"
              onClick={handleResetLayout}
              className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
              title="Restaurar orden y módulos originales"
            >
              Reset
            </button>
          )}
          <button
            type="button"
            onClick={() => {
              setEditMode((v) => !v);
              setShowPicker(false);
            }}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              editMode
                ? "bg-eko-blue text-white hover:bg-eko-blue-dark"
                : "bg-white/5 text-gray-300 hover:bg-white/10 hover:text-white"
            }`}
          >
            {editMode ? (
              <>
                <Check className="w-3.5 h-3.5" />
                Done
              </>
            ) : (
              <>
                <Pencil className="w-3.5 h-3.5" />
                Editar
              </>
            )}
          </button>
        </div>
      </div>

      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={visibleHrefs} strategy={rectSortingStrategy}>
          <div
            className={`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-11 gap-3 ${
              editMode ? "jiggle" : ""
            }`}
          >
            {visibleHrefs.map((href) => {
              const mod = modulesByHref[href];
              const badge = mod.badgeKey === "unread" ? unreadCount : undefined;
              return (
                <SortableModule
                  key={href}
                  mod={mod}
                  badge={badge}
                  editMode={editMode}
                  onRemove={handleRemove}
                />
              );
            })}

            {/* "+" tile in edit mode, only if there are hidden modules to add back */}
            {editMode && hiddenList.length > 0 && (
              <button
                type="button"
                onClick={() => setShowPicker((v) => !v)}
                className="group relative flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-white/10 bg-white/[0.01] p-4 hover:bg-white/[0.04] hover:border-eko-blue/50 transition-all min-h-[112px]"
                title={`Agregar módulo (${hiddenList.length} disponible${hiddenList.length === 1 ? "" : "s"})`}
              >
                <div className="p-2.5 rounded-lg bg-white/5 text-gray-400 group-hover:text-eko-blue transition-colors">
                  <Plus className="w-5 h-5" />
                </div>
                <p className="text-[10px] text-gray-500 group-hover:text-gray-300 transition-colors">
                  Agregar ({hiddenList.length})
                </p>
              </button>
            )}
          </div>
        </SortableContext>
      </DndContext>

      {/* Picker modal — list of hidden modules to re-add */}
      {editMode && showPicker && hiddenList.length > 0 && (
        <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.03] p-4 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-medium text-gray-400 uppercase tracking-wider">
              Módulos disponibles
            </h3>
            <button
              type="button"
              onClick={() => setShowPicker(false)}
              className="text-gray-500 hover:text-white transition-colors"
              aria-label="Cerrar"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2">
            {hiddenList.map((href) => {
              const mod = modulesByHref[href];
              if (!mod) return null;
              return (
                <button
                  key={href}
                  type="button"
                  onClick={() => handleAdd(href)}
                  className="group flex items-center gap-2 rounded-lg border border-white/5 bg-white/[0.02] p-2.5 hover:bg-white/[0.06] hover:border-eko-blue/40 transition-all text-left"
                >
                  <div className={`p-1.5 rounded-md ${mod.color}`}>
                    <mod.icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-white truncate">{mod.label}</p>
                    <p className="text-[10px] text-gray-500 truncate">{mod.subtitle}</p>
                  </div>
                  <Plus className="w-3.5 h-3.5 text-gray-500 group-hover:text-eko-blue transition-colors" />
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
