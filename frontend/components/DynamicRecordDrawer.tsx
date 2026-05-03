"use client";

import { useState, useEffect, useMemo } from "react";
import { X, Loader2, Save } from "lucide-react";
import { ObjectMetadata, FieldMetadata, DynamicRecord } from "@/lib/api";

interface DynamicRecordDrawerProps {
  object: ObjectMetadata;
  record?: DynamicRecord | null;
  open: boolean;
  onClose: () => void;
  onSave: (payload: { label: string; data: Record<string, any> }) => void;
  saving?: boolean;
}

function getInputType(fieldType: string): string {
  switch (fieldType) {
    case "NUMBER":
    case "CURRENCY":
      return "number";
    case "EMAIL":
      return "email";
    case "PHONE":
      return "tel";
    case "URL":
      return "url";
    case "DATE":
      return "date";
    case "DATE_TIME":
      return "datetime-local";
    default:
      return "text";
  }
}

export default function DynamicRecordDrawer({
  object,
  record,
  open,
  onClose,
  onSave,
  saving,
}: DynamicRecordDrawerProps) {
  const [values, setValues] = useState<Record<string, any>>({});
  const [label, setLabel] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const labelField = useMemo(() => object.fields.find((f) => f.is_label_field), [object.fields]);
  const editableFields = useMemo(
    () => object.fields.filter((f) => !f.is_system && !f.is_read_only),
    [object.fields]
  );

  useEffect(() => {
    if (open) {
      if (record) {
        setValues({ ...record.data });
        setLabel(record.label);
      } else {
        const defaults: Record<string, any> = {};
        editableFields.forEach((f) => {
          if (f.default_value != null) {
            defaults[f.name] = f.default_value;
          }
        });
        setValues(defaults);
        setLabel("");
      }
      setErrors({});
    }
  }, [open, record, editableFields]);

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!label.trim()) {
      errs._label = `El campo ${labelField?.label || "nombre"} es obligatorio`;
    }
    editableFields.forEach((field) => {
      if (!field.is_nullable && (values[field.name] == null || values[field.name] === "")) {
        errs[field.name] = `${field.label} es obligatorio`;
      }
      if (field.type === "EMAIL" && values[field.name]) {
        const email = String(values[field.name]);
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          errs[field.name] = "Email inválido";
        }
      }
      if (field.type === "URL" && values[field.name]) {
        const url = String(values[field.name]);
        if (!/^(https?:\/\/)?[^\s/$.?#].[^\s]*$/i.test(url)) {
          errs[field.name] = "URL inválida";
        }
      }
    });
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    onSave({ label: label.trim(), data: values });
  };

  const handleChange = (field: FieldMetadata, value: any) => {
    setValues((prev) => ({ ...prev, [field.name]: value }));
    if (errors[field.name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[field.name];
        return next;
      });
    }
    // Auto-update label if this is the label field
    if (field.is_label_field && typeof value === "string") {
      setLabel(value);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      {/* Drawer */}
      <div className="relative w-full max-w-lg h-full bg-eko-graphite border-l border-white/5 shadow-2xl flex flex-col animate-in slide-in-from-right">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
          <h2 className="text-lg font-bold font-display">
            {record ? `Editar ${object.label_singular}` : `Nuevo ${object.label_singular}`}
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
          {/* Label field */}
          {labelField && (
            <div>
              <label className="block text-sm font-medium mb-1.5">
                {labelField.label}
                {!labelField.is_nullable && <span className="text-red-400 ml-0.5">*</span>}
              </label>
              <input
                type={getInputType(labelField.type)}
                value={label}
                onChange={(e) => {
                  setLabel(e.target.value);
                  if (errors._label) setErrors((p) => { const n = { ...p }; delete n._label; return n; });
                }}
                className={`w-full rounded-lg border bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none transition-colors ${
                  errors._label ? "border-red-500" : "border-white/10"
                }`}
                placeholder={`Ingresa ${labelField.label.toLowerCase()}...`}
              />
              {errors._label && <p className="mt-1 text-xs text-red-400">{errors._label}</p>}
            </div>
          )}

          {/* Other fields */}
          {editableFields
            .filter((f) => !f.is_label_field)
            .sort((a, b) => a.position - b.position)
            .map((field) => (
              <div key={field.id}>
                <label className="block text-sm font-medium mb-1.5">
                  {field.label}
                  {!field.is_nullable && <span className="text-red-400 ml-0.5">*</span>}
                  {field.description && (
                    <span className="block text-xs text-gray-500 font-normal mt-0.5">{field.description}</span>
                  )}
                </label>

                {field.type === "BOOLEAN" ? (
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={!!values[field.name]}
                      onChange={(e) => handleChange(field, e.target.checked)}
                      className="w-4 h-4 rounded border-white/20 bg-white/5 accent-eko-blue"
                    />
                    <span className="text-sm text-gray-300">{field.label}</span>
                  </label>
                ) : field.type === "SELECT" && field.options?.length ? (
                  <select
                    value={values[field.name] ?? ""}
                    onChange={(e) => handleChange(field, e.target.value || null)}
                    className={`w-full rounded-lg border bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none transition-colors ${
                      errors[field.name] ? "border-red-500" : "border-white/10"
                    }`}
                  >
                    <option value="">Seleccionar...</option>
                    {field.options.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                ) : field.type === "MULTI_SELECT" && field.options?.length ? (
                  <div className="space-y-2">
                    {field.options.map((opt) => {
                      const selected = Array.isArray(values[field.name]) ? values[field.name] : [];
                      return (
                        <label key={opt.value} className="flex items-center gap-3 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={selected.includes(opt.value)}
                            onChange={(e) => {
                              const current = Array.isArray(values[field.name]) ? [...values[field.name]] : [];
                              if (e.target.checked) {
                                handleChange(field, [...current, opt.value]);
                              } else {
                                handleChange(field, current.filter((v: string) => v !== opt.value));
                              }
                            }}
                            className="w-4 h-4 rounded border-white/20 bg-white/5 accent-eko-blue"
                          />
                          <span className="text-sm text-gray-300">{opt.label}</span>
                        </label>
                      );
                    })}
                  </div>
                ) : field.type === "TEXT" && field.settings?.multiline ? (
                  <textarea
                    value={values[field.name] ?? ""}
                    onChange={(e) => handleChange(field, e.target.value)}
                    rows={4}
                    className={`w-full rounded-lg border bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none transition-colors resize-none ${
                      errors[field.name] ? "border-red-500" : "border-white/10"
                    }`}
                    placeholder={`Ingresa ${field.label.toLowerCase()}...`}
                  />
                ) : (
                  <input
                    type={getInputType(field.type)}
                    value={values[field.name] ?? ""}
                    onChange={(e) => {
                      const val =
                        field.type === "NUMBER" || field.type === "CURRENCY"
                          ? e.target.value === ""
                            ? null
                            : parseFloat(e.target.value)
                          : e.target.value;
                      handleChange(field, val);
                    }}
                    className={`w-full rounded-lg border bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none transition-colors ${
                      errors[field.name] ? "border-red-500" : "border-white/10"
                    }`}
                    placeholder={`Ingresa ${field.label.toLowerCase()}...`}
                  />
                )}
                {errors[field.name] && <p className="mt-1 text-xs text-red-400">{errors[field.name]}</p>}
              </div>
            ))}
        </form>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-white/5">
          <button
            onClick={onClose}
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-gray-300 hover:bg-white/10 transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="flex items-center gap-2 rounded-lg bg-eko-blue px-4 py-2 text-sm font-medium hover:bg-eko-blue-dark disabled:opacity-50 transition-colors"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            Guardar
          </button>
        </div>
      </div>
    </div>
  );
}
