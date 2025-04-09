{{/*
🔱 OMEGA BTC AI - Divine BTC Oracle Helper Templates 🔱
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "btc-oracle.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "btc-oracle.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "btc-oracle.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "btc-oracle.labels" -}}
helm.sh/chart: {{ include "btc-oracle.chart" . }}
{{ include "btc-oracle.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
omega.ai/divine-origin: "true"
omega.ai/fibonacci-enabled: "true"
{{- end }}

{{/*
Selector labels
*/}}
{{- define "btc-oracle.selectorLabels" -}}
app.kubernetes.io/name: {{ include "btc-oracle.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "btc-oracle.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "btc-oracle.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Divine Backup Annotations
*/}}
{{- define "btc-oracle.backupAnnotations" -}}
{{- if .Values.backup.enabled }}
backup.velero.io/backup-volumes: oracle-data
{{- end }}
{{- end }}

{{/*
Create Redis URI
*/}}
{{- define "btc-oracle.redisURI" -}}
{{- if .Values.redis.enabled -}}
redis://{{ .Release.Name }}-redis-master:6379/0
{{- else if .Values.externalRedis.uri -}}
{{ .Values.externalRedis.uri }}
{{- else -}}
redis://{{ .Values.externalRedis.host }}:{{ .Values.externalRedis.port }}/0
{{- end -}}
{{- end -}} 