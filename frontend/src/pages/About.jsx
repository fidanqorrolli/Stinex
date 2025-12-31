import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { 
  Users, 
  Award, 
  Clock, 
  Shield,
  Heart,
  Star,
  CheckCircle,
  ArrowRight,
  Phone,
  Mail,
  MapPin
} from "lucide-react";

const About = () => {
  const values = [
    {
      icon: Heart,
      title: "Leidenschaft",
      description: "Wir lieben, was wir tun und setzen uns mit Herzblut für perfekte Sauberkeit ein"
    },
    {
      icon: Shield,
      title: "Zuverlässigkeit",
      description: "Pünktlich, vertrauenswürdig und diskret - darauf können Sie sich verlassen"
    },
    {
      icon: Star,
      title: "Qualität",
      description: "Höchste Standards und kontinuierliche Qualitätskontrolle bei jedem Auftrag"
    },
    {
      icon: Users,
      title: "Kundenorientierung",
      description: "Ihre Zufriedenheit steht für uns an erster Stelle - immer und überall"
    }
  ];

  const stats = [
    { number: "500+", label: "Zufriedene Kunden" },
    { number: "10+", label: "Jahre Erfahrung" },
    { number: "50+", label: "Projekte pro Monat" },
    { number: "24/7", label: "Erreichbarkeit" }
  ];

  const team = [
    {
      name: "Anna Stinex",
      role: "Geschäftsführerin",
      description: "Gründerin von Stinex mit über 15 Jahren Erfahrung in der Reinigungsbranche"
    },
    {
      name: "Michael Weber",
      role: "Teamleiter",
      description: "Koordiniert unsere Reinigungsteams und sorgt für höchste Qualitätsstandards"
    },
    {
      name: "Sarah König",
      role: "Kundenbetreuung",
      description: "Ihre Ansprechpartnerin für alle Fragen rund um unsere Dienstleistungen"
    }
  ];

  const certifications = [
    "ISO 9001 Qualitätsmanagement",
    "Berufsgenossenschaft registriert",
    "Vollversichert und boniert",
    "HACCP zertifiziert",
    "Umweltschutz Standards"
  ];

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Über Stinex
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Seit über 10 Jahren sorgen wir für Sauberkeit und Ordnung in Hamburg und Umgebung. 
            Was als kleines Familienunternehmen begann, ist heute ein vertrauensvoller Partner 
            für Hunderte von Kunden.
          </p>
        </div>

        {/* Story Section */}
        <div className="grid lg:grid-cols-2 gap-12 mb-16">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Unsere Geschichte</h2>
            <div className="space-y-4 text-gray-600">
              <p>
                Stinex wurde 2013 von Anna Stinex mit der Vision gegründet, professionelle 
                Reinigungsdienstleistungen zu fairen Preisen anzubieten. Was mit einem kleinen 
                Team von drei Mitarbeitern begann, ist heute ein etabliertes Unternehmen mit 
                über 20 qualifizierten Reinigungskräften.
              </p>
              <p>
                Unser Erfolg basiert auf drei Säulen: erstklassiger Service, faire Preise und 
                absolute Zuverlässigkeit. Diese Werte haben uns zum bevorzugten Partner für 
                Privatkunden, Büros und Gewerbebetriebe in der Region gemacht.
              </p>
              <p>
                Heute reinigen wir regelmäßig über 200 Objekte und haben bereits mehr als 
                1000 Kunden mit einmaligen Reinigungsdienstleistungen geholfen. Dabei bleibt 
                unser Anspruch unverändert: Jeder Kunde soll zu 100% zufrieden sein.
              </p>
            </div>
          </div>
          <div className="bg-blue-50 rounded-xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Zahlen & Fakten</h3>
            <div className="grid grid-cols-2 gap-6">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl font-bold text-emerald-600 mb-2">{stat.number}</div>
                  <div className="text-gray-600">{stat.label}</div>
                </div>
              ))}
            </div>
            <div className="mt-8 pt-6 border-t border-emerald-200">
              <h4 className="font-semibold text-gray-900 mb-4">Zertifizierungen:</h4>
              <div className="space-y-2">
                {certifications.map((cert, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                    <span className="text-sm text-gray-600">{cert}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Values */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Unsere Werte
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const Icon = value.icon;
              return (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow duration-300">
                  <CardContent className="pt-8 pb-6">
                    <div className="w-16 h-16 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Icon className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">{value.title}</h3>
                    <p className="text-gray-600">{value.description}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Team */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Unser Team
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow duration-300">
                <CardContent className="pt-8 pb-6">
                  <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <Users className="h-10 w-10 text-gray-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                  <Badge variant="secondary" className="mb-4">{member.role}</Badge>
                  <p className="text-gray-600">{member.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Mission */}
        <div className="bg-gray-50 rounded-xl p-8 lg:p-12 mb-16">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              Unsere Mission
            </h2>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Wir möchten Ihnen mehr Zeit für die wichtigen Dinge im Leben schenken, 
              indem wir uns um die Sauberkeit kümmern. Dabei setzen wir auf 
              umweltfreundliche Reinigungsmittel, faire Arbeitsbedingungen für 
              unser Team und transparente Preise für unsere Kunden.
            </p>
            <div className="grid md:grid-cols-3 gap-8 text-left">
              <div>
                <Award className="h-8 w-8 text-emerald-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Qualität</h3>
                <p className="text-gray-600 text-sm">
                  Kontinuierliche Weiterbildung und modernste Reinigungstechniken
                </p>
              </div>
              <div>
                <Shield className="h-8 w-8 text-emerald-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Sicherheit</h3>
                <p className="text-gray-600 text-sm">
                  Vollversichert und geprüfte Mitarbeiter für Ihr Vertrauen
                </p>
              </div>
              <div>
                <Heart className="h-8 w-8 text-emerald-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Nachhaltigkeit</h3>
                <p className="text-gray-600 text-sm">
                  Umweltfreundliche Produkte und ressourcenschonende Verfahren
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Contact CTA */}
        <div className="text-center bg-blue-600 rounded-xl p-12">
          <h2 className="text-3xl font-bold text-white mb-4">
            Lernen Sie uns persönlich kennen
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Haben Sie Fragen zu unserem Unternehmen oder möchten Sie ein 
            persönliches Beratungsgespräch? Wir freuen uns auf Ihren Kontakt!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              asChild 
              size="lg" 
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-gray-100"
            >
              <Link to="/contact">
                Kontakt aufnehmen
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button 
              asChild 
              size="lg" 
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-600"
            >
              <Link to="/services">Unsere Leistungen</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;