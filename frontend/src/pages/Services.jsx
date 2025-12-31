import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { 
  Building2, 
  Home, 
  Store, 
  CheckCircle, 
  ArrowRight,
  Calendar,
  Sparkles,
  Users,
  Clock
} from "lucide-react";

const Services = () => {
  const mainServices = [
    {
      icon: Building2,
      title: "Büroreinigung",
      description: "Professionelle Reinigung für Büros, Praxen und Verwaltungsgebäude",
      features: [
        "Tägliche oder wöchentliche Reinigung",
        "Schreibtische und Arbeitsflächen",
        "Sanitäranlagen und Küchen",
        "Staubsaugen und Wischen",
        "Fensterreinigung",
        "Müllentsorgung"
      ],
      pricing: "Ab 15€ pro Stunde",
      color: "bg-blue-50 border-blue-200",
      iconColor: "text-blue-600"
    },
    {
      icon: Home,
      title: "Wohnungsreinigung",
      description: "Gründliche Reinigung für Ihr Zuhause - von der Grundreinigung bis zur regelmäßigen Pflege",
      features: [
        "Grundreinigung bei Umzug",
        "Regelmäßige Haushaltsreinigung",
        "Bad- und Küchenreinigung",
        "Fenster innen und außen",
        "Treppenhaus reinigen",
        "Balkon und Terrasse"
      ],
      pricing: "Ab 25€ pro Stunde",
      color: "bg-green-50 border-green-200",
      iconColor: "text-green-600"
    },
    {
      icon: Store,
      title: "Gewerbereinigung",
      description: "Spezialisierte Reinigung für Geschäfte, Restaurants und Industrieobjekte",
      features: [
        "Ladenlokale und Geschäfte",
        "Restaurants und Cafés",
        "Lagerhallen und Werkstätten",
        "Hotelreinigung",
        "Praxen und Kliniken",
        "Industriereinigung"
      ],
      pricing: "Individuell kalkuliert",
      color: "bg-purple-50 border-purple-200",
      iconColor: "text-purple-600"
    }
  ];

  const additionalServices = [
    {
      icon: Sparkles,
      title: "Grundreinigung",
      description: "Intensive Ersteinigung oder nach Renovierungen"
    },
    {
      icon: Calendar,
      title: "Einmalige Reinigung",
      description: "Flexible Einzeltermine nach Bedarf"
    },
    {
      icon: Users,
      title: "Großobjekte",
      description: "Reinigung großer Gebäudekomplexe"
    },
    {
      icon: Clock,
      title: "24/7 Service",
      description: "Notfallreinigung rund um die Uhr"
    }
  ];

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Unsere Reinigungsleistungen
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Von der kleinen Wohnung bis zum großen Bürogebäude - wir bieten professionelle 
            Reinigungsdienstleistungen für jeden Bedarf. Zuverlässig, gründlich und zu fairen Preisen.
          </p>
        </div>

        {/* Main Services */}
        <div className="space-y-12 mb-16">
          {mainServices.map((service, index) => {
            const Icon = service.icon;
            return (
              <Card key={index} className={`${service.color} hover:shadow-xl transition-all duration-300`}>
                <div className="grid lg:grid-cols-3 gap-8 p-8">
                  <div className="lg:col-span-1">
                    <div className="flex items-center mb-4">
                      <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center mr-4">
                        <Icon className={`h-6 w-6 ${service.iconColor}`} />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900">{service.title}</h3>
                        <Badge variant="secondary" className="mt-1">
                          {service.pricing}
                        </Badge>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-6">{service.description}</p>
                    <Button asChild className="bg-emerald-600 hover:bg-emerald-700">
                      <Link to="/contact">
                        Angebot anfordern
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Link>
                    </Button>
                  </div>
                  <div className="lg:col-span-2">
                    <h4 className="text-lg font-semibold text-gray-900 mb-4">Leistungsumfang:</h4>
                    <div className="grid md:grid-cols-2 gap-3">
                      {service.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center">
                          <CheckCircle className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Additional Services */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
            Weitere Dienstleistungen
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {additionalServices.map((service, index) => {
              const Icon = service.icon;
              return (
                <div key={index} className="text-center p-4 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="w-12 h-12 bg-emerald-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{service.title}</h3>
                  <p className="text-gray-600 text-sm">{service.description}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Process */}
        <div className="bg-gray-50 rounded-xl p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
            So einfach funktioniert's
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Kontakt aufnehmen</h3>
              <p className="text-gray-600">
                Rufen Sie uns an oder senden Sie eine Anfrage über unser Kontaktformular
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Kostenloses Angebot</h3>
              <p className="text-gray-600">
                Wir besichtigen Ihre Räumlichkeiten und erstellen ein maßgeschneidertes Angebot
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Professionelle Reinigung</h3>
              <p className="text-gray-600">
                Unser erfahrenes Team führt die Reinigung zuverlässig und gründlich durch
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-blue-600 rounded-xl p-12">
          <h2 className="text-3xl font-bold text-white mb-4">
            Bereit für professionelle Sauberkeit?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Kontaktieren Sie uns für ein unverbindliches Angebot. 
            Wir finden die perfekte Reinigungslösung für Ihre Bedürfnisse.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              asChild 
              size="lg" 
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-gray-100"
            >
              <Link to="/contact">Kostenlos anfragen</Link>
            </Button>
            <Button 
              asChild 
              size="lg" 
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-600"
            >
              <Link to="/about">Über uns erfahren</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Services;