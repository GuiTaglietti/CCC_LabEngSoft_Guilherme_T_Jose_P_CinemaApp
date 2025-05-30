<template>
  <div class="relatorio-container">
    <h1 class="relatorio-title">
      <i class="bi bi-bar-chart me-2"></i> Relatórios de Gestão
    </h1>
    <el-button type="danger" @click="gerarRelatorio">
      <i class="bi bi-file-earmark-pdf me-2"></i> Gerar Relatório PDF
    </el-button>
  </div>
</template>

<script setup>
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import axios from "axios";
import { ElMessage } from "element-plus";

const gerarRelatorio = async () => {
  try {
    const [ingressosRes, sessoesRes] = await Promise.all([
      axios.get("http://localhost:5000/api/tickets/all"),
      axios.get("http://localhost:5000/api/sessions"),
    ]);

    const ingressos = ingressosRes.data;
    const sessoes = sessoesRes.data;

    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text("Relatório de Gestão - Cinema", 14, 22);

    doc.setFontSize(14);
    doc.text("Ingressos:", 14, 35);

    autoTable(doc, {
      startY: 40,
      head: [["ID", "Filme", "Assento", "Status"]],
      body: ingressos.map((i) => [
        i.id,
        i.title,
        i.seat_number,
        i.payment_status,
      ]),
    });

    doc.text("Sessões:", 14, doc.lastAutoTable.finalY + 10);

    autoTable(doc, {
      startY: doc.lastAutoTable.finalY + 15,
      head: [["ID", "Filme", "Sala", "Início", "Fim"]],
      body: sessoes.map((s) => [
        s.id,
        s.movie_title,
        s.room,
        s.start_time,
        s.end_time,
      ]),
    });

    doc.save("relatorio_cinema.pdf");
    ElMessage.success("Relatório gerado com sucesso!");
  } catch (error) {
    console.error(error);
    ElMessage.error("Erro ao gerar relatório");
  }
};
</script>

<style scoped>
.relatorio-container {
  padding: 2rem;
  background-color: #1a1a1a;
  border-radius: 1rem;
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
  color: white;
  text-align: center;
}

.relatorio-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.el-button {
  background-color: #ff0000;
  color: white;
  font-weight: bold;
}
</style>
