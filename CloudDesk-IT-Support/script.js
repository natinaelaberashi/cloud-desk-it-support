const tickets = [
  {
    id: "TCK-1048",
    title: "VPN access not reconnecting after MFA reset",
    requester: "Alicia Johnson",
    department: "IT Support",
    priority: "High",
    status: "In Progress",
    assignee: "N. Smith",
    created: "2026-09-02",
    description: "User can authenticate but loses VPN session after password change. Needs remote access validation."
  },
  {
    id: "TCK-1049",
    title: "File server storage nearing threshold",
    requester: "Marcus Lee",
    department: "Infrastructure",
    priority: "Medium",
    status: "Open",
    assignee: "D. Patel",
    created: "2026-09-03",
    description: "Storage reports 88% usage with nightly backups starting to queue."
  },
  {
    id: "TCK-1050",
    title: "Laptop replacement request for Finance team",
    requester: "Nora Chen",
    department: "Finance",
    priority: "Low",
    status: "Resolved",
    assignee: "J. Rivera",
    created: "2026-08-29",
    description: "Device replacement approved and delivered to user."
  },
  {
    id: "TCK-1051",
    title: "Email delivery delays for customer portal",
    requester: "Samuel Kim",
    department: "Security",
    priority: "Critical",
    status: "Blocked",
    assignee: "L. Morgan",
    created: "2026-09-04",
    description: "Mail queue backlog impacting onboarding and customer notifications."
  },
  {
    id: "TCK-1052",
    title: "New employee onboarding account setup",
    requester: "Priya Nair",
    department: "HR",
    priority: "Medium",
    status: "Open",
    assignee: "R. Davis",
    created: "2026-09-04",
    description: "Need access to Microsoft 365, VPN, and internal ticketing system for a new hire."
  }
];

const state = {
  search: "",
  status: "all",
  priority: "all"
};

const ticketTableBody = document.getElementById("ticketTableBody");
const totals = {
  total: document.getElementById("totalTickets"),
  open: document.getElementById("openTickets"),
  progress: document.getElementById("progressTickets"),
  resolved: document.getElementById("resolvedTickets")
};
const ticketCount = document.getElementById("ticketCount");
const ticketForm = document.getElementById("ticketForm");
const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");
const priorityFilter = document.getElementById("priorityFilter");

function badgeClass(value, type) {
  const normalized = value.toLowerCase().replace(/\s+/g, "");
  return `${type} ${normalized}`;
}

function renderStats() {
  const open = tickets.filter((ticket) => ticket.status === "Open").length;
  const progress = tickets.filter((ticket) => ticket.status === "In Progress").length;
  const resolved = tickets.filter((ticket) => ticket.status === "Resolved").length;

  totals.total.textContent = tickets.length;
  totals.open.textContent = open;
  totals.progress.textContent = progress;
  totals.resolved.textContent = resolved;
}

function getFilteredTickets() {
  return tickets.filter((ticket) => {
    const query = state.search.trim().toLowerCase();
    const matchesSearch =
      !query ||
      [ticket.id, ticket.title, ticket.requester, ticket.assignee, ticket.department]
        .join(" ")
        .toLowerCase()
        .includes(query);

    const matchesStatus = state.status === "all" || ticket.status === state.status;
    const matchesPriority = state.priority === "all" || ticket.priority === state.priority;

    return matchesSearch && matchesStatus && matchesPriority;
  });
}

function renderTable() {
  const filteredTickets = getFilteredTickets();
  ticketCount.textContent = `${filteredTickets.length} item${filteredTickets.length === 1 ? "" : "s"}`;

  if (!filteredTickets.length) {
    ticketTableBody.innerHTML = `
      <tr>
        <td colspan="8" class="empty-state">No tickets match the current filters.</td>
      </tr>
    `;
    return;
  }

  ticketTableBody.innerHTML = filteredTickets
    .map(
      (ticket) => `
        <tr>
          <td>${ticket.id}</td>
          <td>${ticket.title}</td>
          <td>${ticket.requester}</td>
          <td>${ticket.department}</td>
          <td><span class="badge ${badgeClass(ticket.priority, "priority")}">${ticket.priority}</span></td>
          <td><span class="badge ${badgeClass(ticket.status, "status")}">${ticket.status}</span></td>
          <td>${ticket.assignee}</td>
          <td>${ticket.created}</td>
        </tr>
      `
    )
    .join("");
}

function render() {
  renderStats();
  renderTable();
}

searchInput.addEventListener("input", (event) => {
  state.search = event.target.value;
  renderTable();
});

statusFilter.addEventListener("change", (event) => {
  state.status = event.target.value;
  renderTable();
});

priorityFilter.addEventListener("change", (event) => {
  state.priority = event.target.value;
  renderTable();
});

ticketForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const newTicket = {
    id: `TCK-${Math.floor(1000 + Math.random() * 9000)}`,
    title: document.getElementById("ticketTitle").value.trim(),
    requester: document.getElementById("requester").value.trim(),
    department: document.getElementById("department").value,
    priority: document.getElementById("priority").value,
    status: document.getElementById("status").value,
    assignee: document.getElementById("assignee").value.trim(),
    created: new Date().toISOString().slice(0, 10),
    description: document.getElementById("description").value.trim()
  };

  if (!newTicket.title || !newTicket.requester || !newTicket.assignee) {
    return;
  }

  tickets.unshift(newTicket);
  ticketForm.reset();
  render();
});

render();
